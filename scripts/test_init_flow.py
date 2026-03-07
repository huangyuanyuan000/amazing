#!/usr/bin/env python3
"""
测试完整初始化流程

验证 Amazing 脚手架的所有功能
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import tempfile


class InitFlowTest:
    """初始化流程测试"""

    def __init__(self):
        self.framework_path = Path(__file__).parent.parent
        self.test_dir = None
        self.test_project = "test-project"
        self.passed = 0
        self.failed = 0

    def setup(self):
        """准备测试环境"""
        print("🔧 准备测试环境...")
        self.test_dir = Path(tempfile.mkdtemp(prefix="amazing-test-"))
        print(f"  测试目录: {self.test_dir}")

    def cleanup(self):
        """清理测试环境"""
        if self.test_dir and self.test_dir.exists():
            print(f"\n🧹 清理测试环境: {self.test_dir}")
            shutil.rmtree(self.test_dir)

    def run_command(self, cmd, cwd=None):
        """运行命令"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or self.test_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "命令超时"
        except Exception as e:
            return False, "", str(e)

    def test_orchestrator_exists(self):
        """测试 orchestrator 是否存在"""
        print("\n📋 测试 1: 检查 orchestrator...")
        orchestrator = self.framework_path / "scripts" / "orchestrator.py"

        if orchestrator.exists():
            print("  ✓ orchestrator.py 存在")
            self.passed += 1
            return True
        else:
            print("  ✗ orchestrator.py 不存在")
            self.failed += 1
            return False

    def test_handoff_manager_exists(self):
        """测试 handoff_manager 是否存在"""
        print("\n📋 测试 2: 检查 handoff_manager...")
        manager = self.framework_path / "scripts" / "handoff_manager.py"

        if manager.exists():
            print("  ✓ handoff_manager.py 存在")
            self.passed += 1
            return True
        else:
            print("  ✗ handoff_manager.py 不存在")
            self.failed += 1
            return False

    def test_handoff_agents_exist(self):
        """测试 handoff agents 是否存在"""
        print("\n📋 测试 3: 检查 handoff agents...")
        agents_dir = self.framework_path / ".agents" / "init-handoffs"

        required_agents = [
            "page-generator",
            "service-generator",
            "store-generator",
            "model-generator",
            "api-generator",
            "test-generator"
        ]

        all_exist = True
        for agent in required_agents:
            agent_path = agents_dir / agent
            if agent_path.exists():
                print(f"  ✓ {agent}")
            else:
                print(f"  ✗ {agent} 不存在")
                all_exist = False

        if all_exist:
            self.passed += 1
        else:
            self.failed += 1

        return all_exist

    def test_init_phases_exist(self):
        """测试初始化阶段脚本是否存在"""
        print("\n📋 测试 4: 检查初始化阶段脚本...")
        phases_dir = self.framework_path / "scripts" / "phases"

        required_phases = [
            "structure_init.py",
            "handoffs_setup.py",
            "role_config.py",
            "business_agent_gen.py",
            "backend_gen.py",
            "frontend_gen.py",
            "deploy_gen.py",
            "docs_gen.py"
        ]

        all_exist = True
        for phase in required_phases:
            phase_path = phases_dir / phase
            if phase_path.exists():
                print(f"  ✓ {phase}")
            else:
                print(f"  ✗ {phase} 不存在")
                all_exist = False

        if all_exist:
            self.passed += 1
        else:
            self.failed += 1

        return all_exist

    def test_init_script_syntax(self):
        """测试 init.py 语法"""
        print("\n📋 测试 5: 检查 init.py 语法...")
        init_script = self.framework_path / "scripts" / "init.py"

        success, stdout, stderr = self.run_command(
            f"python3 -m py_compile {init_script}",
            cwd=self.framework_path
        )

        if success:
            print("  ✓ init.py 语法正确")
            self.passed += 1
            return True
        else:
            print(f"  ✗ init.py 语法错误: {stderr}")
            self.failed += 1
            return False

    def test_orchestrator_syntax(self):
        """测试 orchestrator.py 语法"""
        print("\n📋 测试 6: 检查 orchestrator.py 语法...")
        orchestrator = self.framework_path / "scripts" / "orchestrator.py"

        success, stdout, stderr = self.run_command(
            f"python3 -m py_compile {orchestrator}",
            cwd=self.framework_path
        )

        if success:
            print("  ✓ orchestrator.py 语法正确")
            self.passed += 1
            return True
        else:
            print(f"  ✗ orchestrator.py 语法错误: {stderr}")
            self.failed += 1
            return False

    def test_example_structure(self):
        """测试案例结构"""
        print("\n📋 测试 7: 检查案例结构...")
        example_dir = self.framework_path / "examples" / "model-platform"

        required_dirs = [
            ".claude/roles",
            ".claude/ironclaw",
            ".agents/handoffs",
            "deploy/k8s",
            "deploy/offline"
        ]

        all_exist = True
        for dir_path in required_dirs:
            full_path = example_dir / dir_path
            if full_path.exists():
                print(f"  ✓ {dir_path}")
            else:
                print(f"  ✗ {dir_path} 不存在")
                all_exist = False

        if all_exist:
            self.passed += 1
        else:
            self.failed += 1

        return all_exist

    def test_roles_config(self):
        """测试角色配置"""
        print("\n📋 测试 8: 检查角色配置...")
        roles_dir = self.framework_path / "examples" / "model-platform" / ".claude" / "roles"

        required_roles = [
            "architect",
            "product-manager",
            "frontend-dev",
            "backend-dev",
            "test-engineer",
            "devops-engineer",
            "operations"
        ]

        all_exist = True
        for role in required_roles:
            role_config = roles_dir / role / "config.yml"
            if role_config.exists():
                print(f"  ✓ {role}/config.yml")
            else:
                print(f"  ✗ {role}/config.yml 不存在")
                all_exist = False

        if all_exist:
            self.passed += 1
        else:
            self.failed += 1

        return all_exist

    def test_k8s_deployment(self):
        """测试 K8s 部署配置"""
        print("\n📋 测试 9: 检查 K8s 部署配置...")
        k8s_dir = self.framework_path / "examples" / "model-platform" / "deploy" / "k8s"

        required_files = [
            "namespace.yaml",
            "configmap.yaml",
            "secret.yaml",
            "deployment.yaml",
            "service.yaml",
            "ingress.yaml",
            "hpa.yaml",
            "gpu-operator.md",
            "README.md"
        ]

        all_exist = True
        for file in required_files:
            file_path = k8s_dir / file
            if file_path.exists():
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} 不存在")
                all_exist = False

        if all_exist:
            self.passed += 1
        else:
            self.failed += 1

        return all_exist

    def test_offline_deployment(self):
        """测试离线部署配置"""
        print("\n📋 测试 10: 检查离线部署配置...")
        offline_dir = self.framework_path / "examples" / "model-platform" / "deploy" / "offline"

        required_files = [
            "build.sh",
            "install.sh",
            "upgrade.sh",
            "uninstall.sh",
            "README.md"
        ]

        all_exist = True
        for file in required_files:
            file_path = offline_dir / file
            if file_path.exists():
                # 检查是否有执行权限
                if file.endswith('.sh'):
                    if os.access(file_path, os.X_OK):
                        print(f"  ✓ {file} (可执行)")
                    else:
                        print(f"  ⚠️  {file} (无执行权限)")
                else:
                    print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} 不存在")
                all_exist = False

        if all_exist:
            self.passed += 1
        else:
            self.failed += 1

        return all_exist

    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("Amazing 脚手架 - 完整性测试")
        print("=" * 60)

        try:
            self.setup()

            # 运行所有测试
            self.test_orchestrator_exists()
            self.test_handoff_manager_exists()
            self.test_handoff_agents_exist()
            self.test_init_phases_exist()
            self.test_init_script_syntax()
            self.test_orchestrator_syntax()
            self.test_example_structure()
            self.test_roles_config()
            self.test_k8s_deployment()
            self.test_offline_deployment()

            # 显示结果
            print("\n" + "=" * 60)
            print("测试结果")
            print("=" * 60)
            print(f"✓ 通过: {self.passed}")
            print(f"✗ 失败: {self.failed}")
            print(f"总计: {self.passed + self.failed}")

            if self.failed == 0:
                print("\n🎉 所有测试通过！")
                return 0
            else:
                print(f"\n❌ {self.failed} 个测试失败")
                return 1

        finally:
            self.cleanup()


def main():
    """主函数"""
    tester = InitFlowTest()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
