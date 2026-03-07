#!/usr/bin/env python3
"""
IronClaw CLI - 权限管理工具
"""

import argparse
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class IronClawCLI:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.ironclaw_dir = project_root / ".claude" / "ironclaw"
        self.instances_dir = self.ironclaw_dir / "instances"
        self.permissions_file = self.ironclaw_dir / "permissions.yml"
        self.audit_log_file = self.ironclaw_dir / "audit.log"

        # 确保目录存在
        self.instances_dir.mkdir(parents=True, exist_ok=True)

    def request_role(self, role: str, reason: str, experience: str):
        """申请角色"""
        request_id = self._generate_request_id()
        request = {
            "id": request_id,
            "applicant": self._get_current_user(),
            "role": role,
            "reason": reason,
            "experience": experience,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
        }

        # 保存申请
        requests_file = self.ironclaw_dir / "role_requests.yml"
        requests = self._load_yaml(requests_file) or []
        requests.append(request)
        self._save_yaml(requests_file, requests)

        print(f"✅ 角色申请已提交")
        print(f"   申请 ID: {request_id}")
        print(f"   角色: {role}")
        print(f"   状态: 等待架构师审批")

    def list_requests(self, status: Optional[str] = None):
        """列出角色申请"""
        requests_file = self.ironclaw_dir / "role_requests.yml"
        requests = self._load_yaml(requests_file) or []

        if status:
            requests = [r for r in requests if r["status"] == status]

        if not requests:
            print("📭 没有角色申请")
            return

        print(f"\n📋 角色申请列表 ({len(requests)} 个)")
        print("=" * 80)
        for req in requests:
            print(f"ID: {req['id']}")
            print(f"申请人: {req['applicant']}")
            print(f"角色: {req['role']}")
            print(f"理由: {req['reason']}")
            print(f"状态: {req['status']}")
            print(f"时间: {req['created_at']}")
            print("-" * 80)

    def approve_request(self, request_id: str):
        """审批角色申请"""
        # 检查是否是架构师
        if not self._is_architect():
            print("❌ 只有架构师可以审批角色申请")
            return

        requests_file = self.ironclaw_dir / "role_requests.yml"
        requests = self._load_yaml(requests_file) or []

        # 查找申请
        request = None
        for req in requests:
            if req["id"] == request_id:
                request = req
                break

        if not request:
            print(f"❌ 未找到申请: {request_id}")
            return

        if request["status"] != "pending":
            print(f"❌ 申请状态不是 pending: {request['status']}")
            return

        # 更新状态
        request["status"] = "approved"
        request["approved_by"] = self._get_current_user()
        request["approved_at"] = datetime.now().isoformat()
        self._save_yaml(requests_file, requests)

        # 创建角色实例
        self._create_role_instance(
            user=request["applicant"],
            role=request["role"],
            granted_by=request["approved_by"]
        )

        # 记录审计日志
        self._log_audit(
            action="approve_role_request",
            target=request_id,
            details=request
        )

        print(f"✅ 已批准角色申请")
        print(f"   申请人: {request['applicant']}")
        print(f"   角色: {request['role']}")
        print(f"   权限已分配")

    def reject_request(self, request_id: str, reason: str):
        """拒绝角色申请"""
        # 检查是否是架构师
        if not self._is_architect():
            print("❌ 只有架构师可以审批角色申请")
            return

        requests_file = self.ironclaw_dir / "role_requests.yml"
        requests = self._load_yaml(requests_file) or []

        # 查找申请
        request = None
        for req in requests:
            if req["id"] == request_id:
                request = req
                break

        if not request:
            print(f"❌ 未找到申请: {request_id}")
            return

        # 更新状态
        request["status"] = "rejected"
        request["rejected_by"] = self._get_current_user()
        request["rejected_at"] = datetime.now().isoformat()
        request["reject_reason"] = reason
        self._save_yaml(requests_file, requests)

        # 记录审计日志
        self._log_audit(
            action="reject_role_request",
            target=request_id,
            details=request
        )

        print(f"❌ 已拒绝角色申请")
        print(f"   申请人: {request['applicant']}")
        print(f"   角色: {request['role']}")
        print(f"   原因: {reason}")

    def check_permission(self, action: str, target: str, user: Optional[str] = None):
        """检查权限"""
        user = user or self._get_current_user()

        # 加载用户实例
        instance = self._load_user_instance(user)
        if not instance:
            print(f"❌ 用户未分配角色: {user}")
            return False

        # 检查权限
        has_permission = self._check_permission(instance, action, target)

        if has_permission:
            print(f"✅ 有权限")
            print(f"   用户: {user}")
            print(f"   角色: {instance['role']}")
            print(f"   操作: {action}")
            print(f"   目标: {target}")
        else:
            print(f"❌ 无权限")
            print(f"   用户: {user}")
            print(f"   角色: {instance['role']}")
            print(f"   操作: {action}")
            print(f"   目标: {target}")

        return has_permission

    def list_roles(self):
        """列出所有角色实例"""
        instances = list(self.instances_dir.glob("*.yml"))

        if not instances:
            print("📭 没有角色实例")
            return

        print(f"\n👥 角色实例列表 ({len(instances)} 个)")
        print("=" * 80)
        for instance_file in instances:
            instance = self._load_yaml(instance_file)
            print(f"用户: {instance['user']}")
            print(f"角色: {instance['role']}")
            print(f"级别: {instance['level']}")
            print(f"授予时间: {instance['granted_at']}")
            print(f"授予人: {instance['granted_by']}")
            print("-" * 80)

    def revoke_role(self, user: str):
        """撤销角色"""
        # 检查是否是架构师
        if not self._is_architect():
            print("❌ 只有架构师可以撤销角色")
            return

        instance_file = self.instances_dir / f"{user.replace('@', '-').replace('.', '-')}.yml"
        if not instance_file.exists():
            print(f"❌ 用户未分配角色: {user}")
            return

        instance = self._load_yaml(instance_file)

        # 删除实例文件
        instance_file.unlink()

        # 记录审计日志
        self._log_audit(
            action="revoke_role",
            target=user,
            details=instance
        )

        print(f"✅ 已撤销角色")
        print(f"   用户: {user}")
        print(f"   角色: {instance['role']}")

    def view_audit_log(self, limit: int = 50):
        """查看审计日志"""
        if not self.audit_log_file.exists():
            print("📭 没有审计日志")
            return

        logs = self._load_yaml(self.audit_log_file) or []
        logs = logs[-limit:]  # 最近的 N 条

        print(f"\n📜 审计日志 (最近 {len(logs)} 条)")
        print("=" * 80)
        for log in logs:
            print(f"时间: {log['timestamp']}")
            print(f"用户: {log['user']}")
            print(f"操作: {log['action']}")
            print(f"目标: {log['target']}")
            print(f"结果: {log['result']}")
            if "reason" in log:
                print(f"原因: {log['reason']}")
            print("-" * 80)

    # 辅助方法

    def _generate_request_id(self) -> str:
        """生成申请 ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"REQ-{timestamp}"

    def _get_current_user(self) -> str:
        """获取当前用户"""
        # TODO: 从环境变量或配置文件获取
        return "current-user@example.com"

    def _is_architect(self) -> bool:
        """检查是否是架构师"""
        user = self._get_current_user()
        instance = self._load_user_instance(user)
        return instance and instance.get("role") == "architect"

    def _load_user_instance(self, user: str) -> Optional[Dict]:
        """加载用户实例"""
        instance_file = self.instances_dir / f"{user.replace('@', '-').replace('.', '-')}.yml"
        if not instance_file.exists():
            return None
        return self._load_yaml(instance_file)

    def _create_role_instance(self, user: str, role: str, granted_by: str):
        """创建角色实例"""
        # 加载角色权限
        permissions = self._load_yaml(self.permissions_file)
        role_permissions = permissions["roles"].get(role, {})

        instance = {
            "user": user,
            "role": role,
            "level": role_permissions.get("level", "viewer"),
            "granted_at": datetime.now().isoformat(),
            "granted_by": granted_by,
            "expires_at": None,
            "permissions": role_permissions.get("permissions", {}),
            "restrictions": role_permissions.get("restrictions", []),
            "audit_log": []
        }

        instance_file = self.instances_dir / f"{user.replace('@', '-').replace('.', '-')}.yml"
        self._save_yaml(instance_file, instance)

    def _check_permission(self, instance: Dict, action: str, target: str) -> bool:
        """检查权限"""
        permissions = instance.get("permissions", {})

        # 检查是否有该操作的权限
        if action not in permissions:
            return False

        allowed_targets = permissions[action]

        # 如果是 "*"，表示全局权限
        if allowed_targets == "*" or "*" in allowed_targets:
            return True

        # 检查目标是否在允许列表中
        for allowed in allowed_targets:
            if target.startswith(allowed):
                return True

        return False

    def _log_audit(self, action: str, target: str, details: Dict, result: str = "success"):
        """记录审计日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": self._get_current_user(),
            "action": action,
            "target": target,
            "details": details,
            "result": result
        }

        logs = self._load_yaml(self.audit_log_file) or []
        logs.append(log_entry)
        self._save_yaml(self.audit_log_file, logs)

    def _load_yaml(self, file_path: Path) -> Optional[Dict]:
        """加载 YAML 文件"""
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _save_yaml(self, file_path: Path, data: Dict):
        """保存 YAML 文件"""
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(description="IronClaw CLI - 权限管理工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # request-role
    request_parser = subparsers.add_parser("request-role", help="申请角色")
    request_parser.add_argument("--role", required=True, help="角色名称")
    request_parser.add_argument("--reason", required=True, help="申请理由")
    request_parser.add_argument("--experience", default="", help="相关经验")

    # list-requests
    list_requests_parser = subparsers.add_parser("list-requests", help="列出角色申请")
    list_requests_parser.add_argument("--status", help="过滤状态")

    # approve-request
    approve_parser = subparsers.add_parser("approve-request", help="批准角色申请")
    approve_parser.add_argument("--id", required=True, help="申请 ID")

    # reject-request
    reject_parser = subparsers.add_parser("reject-request", help="拒绝角色申请")
    reject_parser.add_argument("--id", required=True, help="申请 ID")
    reject_parser.add_argument("--reason", required=True, help="拒绝原因")

    # check-permission
    check_parser = subparsers.add_parser("check-permission", help="检查权限")
    check_parser.add_argument("--action", required=True, help="操作")
    check_parser.add_argument("--target", required=True, help="目标")
    check_parser.add_argument("--user", help="用户")

    # list-roles
    subparsers.add_parser("list-roles", help="列出所有角色")

    # revoke-role
    revoke_parser = subparsers.add_parser("revoke-role", help="撤销角色")
    revoke_parser.add_argument("--user", required=True, help="用户")

    # view-audit-log
    audit_parser = subparsers.add_parser("view-audit-log", help="查看审计日志")
    audit_parser.add_argument("--limit", type=int, default=50, help="显示条数")

    args = parser.parse_args()

    # 获取项目根目录
    project_root = Path.cwd()
    cli = IronClawCLI(project_root)

    # 执行命令
    if args.command == "request-role":
        cli.request_role(args.role, args.reason, args.experience)
    elif args.command == "list-requests":
        cli.list_requests(args.status)
    elif args.command == "approve-request":
        cli.approve_request(args.id)
    elif args.command == "reject-request":
        cli.reject_parser(args.id, args.reason)
    elif args.command == "check-permission":
        cli.check_permission(args.action, args.target, args.user)
    elif args.command == "list-roles":
        cli.list_roles()
    elif args.command == "revoke-role":
        cli.revoke_role(args.user)
    elif args.command == "view-audit-log":
        cli.view_audit_log(args.limit)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
