import unittest
import os
from main import replace_content_with_sprites  # Replace 'your_module' with the actual name of your module


class TestReplaceContentWithSprites(unittest.TestCase):

    def test_replace_content_with_sprites(self):
        test_cases = [
            {
                'input_path': r'd:\git\succession_wars\Mods\MyMod\Content\Animations\my_animation.json',
                'expected_output': r'd:git\succession_wars\Mods\MyMod\Content\sprites',
            },
            {
                'input_path': r'd:\git\succession_wars\Mods\MyMod\content\config\subdir1\subdir2\etc\my_animation.json',
                'expected_output': r'd:git\succession_wars\Mods\MyMod\content\sprites',
            },
            # Add more test cases as needed
        ]

        for test_case in test_cases:
            with self.subTest(input_path=test_case['input_path']):
                result = replace_content_with_sprites(test_case['input_path'])
                expected_output = test_case['expected_output']
                self.assertEqual(expected_output, result)


if __name__ == '__main__':
    unittest.main()
