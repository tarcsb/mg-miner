import unittest
import os
import shutil
from io import StringIO
from mg_miner.cli import (
    load_config,
    is_excluded,
    get_project_type,
    is_text_file,
    collect_files,
    detect_component,
    summarize_optional_dirs,
    redact_sensitive_info,
    create_summary,
    concatenate_files,
    main
)

class TestMgMiner(unittest.TestCase):
    """
    Test suite for the mg-miner project.
    """

    @classmethod
    def setUpClass(cls):
        """
        Create a temporary directory with test files for the test cases.
        """
        os.makedirs('test_dir', exist_ok=True)
        with open('test_dir/test1.py', 'w') as f:
            f.write("# Test Python file")
        with open('test_dir/test2.js', 'w') as f:
            f.write("// Test JavaScript file")
        with open('test_dir/README.md', 'w') as f:
            f.write("# README")
        os.makedirs('test_dir/.git', exist_ok=True)
        with open('test_dir/.git/config', 'w') as f:
            f.write("[core]\nrepositoryformatversion = 0")
        with open('test_dir/secret.txt', 'w') as f:
            f.write("password=secretpassword\nkey=secretkey")

    @classmethod
    def tearDownClass(cls):
        """
        Remove the temporary directory and its contents after tests are done.
        """
        shutil.rmtree('test_dir')

    def setUp(self):
        """
        Load configuration before each test case.
        """
        self.config = load_config('mg_miner/config.json')

    def test_load_config(self):
        """
        Test if the configuration file is loaded correctly.
        """
        self.assertIn('excluded_dirs', self.config)
        self.assertIn('excluded_extensions', self.config)

    def test_is_excluded(self):
        """
        Test if files are correctly excluded based on directory names.
        """
        self.assertTrue(is_excluded('.git/file', self.config['excluded_dirs']))
        self.assertFalse(is_excluded('src/file', self.config['excluded_dirs']))

    def test_get_project_type(self):
        """
        Test if the project type is correctly identified based on files present.
        """
        files = ['main.py', 'utils.py', 'setup.py']
        project_type = get_project_type(files, self.config['project_types'])
        self.assertEqual(project_type[0][0], 'Python')
        self.assertGreaterEqual(project_type[0][1], 0.1)

    def test_is_text_file(self):
        """
        Test if a file is correctly identified as a text file.
        """
        self.assertTrue(is_text_file(__file__))

    def test_collect_files(self):
        """
        Test collecting files from a directory, excluding specified directories and extensions.
        """
        files, remnants = collect_files('test_dir', self.config['excluded_dirs'], self.config['excluded_extensions'])
        self.assertGreater(len(files), 0)

    def test_collect_files_permissions_error(self):
        """
        Test handling of permissions errors during file collection.
        """
        with open('test_dir/test_file.txt', 'w') as f:
            f.write('test content')
        os.chmod('test_dir/test_file.txt', 0o000)  # No permissions
        files, remnants = collect_files('test_dir', self.config['excluded_dirs'], self.config['excluded_extensions'])
        os.chmod('test_dir/test_file.txt', 0o644)  # Restore permissions
        os.remove('test_dir/test_file.txt')
        self.assertIn('test_dir/test_file.txt', remnants)

    def test_detect_component(self):
        """
        Test detection of backend and frontend components in the project.
        """
        files = ['test_dir/test1.py', 'test_dir/test2.js']
        backend = detect_component(files, self.config['backend_indicators'])
        self.assertIn('Python', backend)
        frontend = detect_component(files, self.config['frontend_indicators'])
        self.assertIn('JavaScript', frontend)

    def test_detect_component_undetermined(self):
        """
        Test handling cases where the component cannot be determined.
        """
        files = ['README.md']
        backend = detect_component(files, self.config['backend_indicators'])
        self.assertIn('Undetermined', backend)
        frontend = detect_component(files, self.config['frontend_indicators'])
        self.assertIn('Undetermined', frontend)
        testing = detect_component(files, self.config['testing_frameworks'])
        self.assertIn('Undetermined', testing)

    def test_summarize_optional_dirs(self):
        """
        Test summarizing the contents of optional directories.
        """
        summaries = summarize_optional_dirs('test_dir', self.config['optional_dirs'])
        self.assertIsInstance(summaries, dict)

    def test_redact_sensitive_info(self):
        """
        Test redaction of sensitive information from files.
        """
        redacted_files = redact_sensitive_info(['test_dir/secret.txt'])
        self.assertIsInstance(redacted_files, list)
        self.assertEqual(redacted_files[0][1], 'password=REDACTED\nkey=REDACTED')

    def test_create_summary(self):
        """
        Test creating a summary of the project.
        """
        files = ['test_dir/test1.py', 'test_dir/test2.js', 'test_dir/README.md']
        project_type = get_project_type(files, self.config['project_types'])
        backend = detect_component(files, self.config['backend_indicators'])
        frontend = detect_component(files, self.config['frontend_indicators'])
        testing = detect_component(files, self.config['testing_frameworks'])
        summary = create_summary(files, project_type, backend, frontend, testing)
        self.assertIn('Project Type', summary)
        self.assertIn('Number of source files', summary)
        self.assertIn('Backend components', summary)
        self.assertIn('Frontend components', summary)
        self.assertIn('Testing frameworks', summary)

    def test_concatenate_files(self):
        """
        Test concatenating multiple files into a single output file.
        """
        concatenate_files(['test_dir/test1.py', 'test_dir/test2.js'], 'test_dir/concatenated_output.txt')
        with open('test_dir/concatenated_output.txt', 'r') as f:
            content = f.read()
        self.assertIn('===== Start of test_dir/test1.py =====', content)
        self.assertIn('===== End of test_dir/test1.py =====', content)
        self.assertIn('===== Start of test_dir/test2.js =====', content)
        self.assertIn('===== End of test_dir/test2.js =====', content)
        os.remove('test_dir/concatenated_output.txt')

    def test_silent_mode(self):
        """
        Test running the script in silent mode.
        """
        import sys
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            main(['--root_dir', 'test_dir', '--silent'])
            output = out.getvalue().strip()
            self.assertEqual(output, "")
        finally:
            sys.stdout = saved_stdout

if __name__ == '__main__':
    unittest.main()
