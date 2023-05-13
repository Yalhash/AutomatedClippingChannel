import unittest
import videoDownload



class HelpersTest(unittest.TestCase):
    '''
        Tests all of the helper functions in videoDownload
    '''
    def test_get_whitelisted_file_name(self):
        '''
            Tests get_whitelisted_file_name
        '''
        case_1_in = "fine_name"
        case_1_exp = case_1_in
        case_2_in = "123 test &^%$#case"
        case_2_exp = "123_test______case"
        case_3_in  = r"\ \ \\ banana"
        case_3_exp  = "_______banana"
        self.assertEqual(videoDownload.get_whitelisted_file_name(case_1_in), case_1_exp)
        self.assertEqual(videoDownload.get_whitelisted_file_name(case_2_in), case_2_exp)
        self.assertEqual(videoDownload.get_whitelisted_file_name(case_3_in), case_3_exp)

    def test_get_clean_unique_file_name(self):
        '''
            Tests get_clean_unique_file_name
        '''
        known_files = set()
        case_1_in = "fine_name"
        case_1_exp = case_1_in
        case_2_in = "fine name"
        case_2_exp = "fine_name_1"
        case_3_in = "fine%name"
        case_3_exp = "fine_name_2"
        case_4_in = "fine  name"
        case_4_exp = "fine__name"

        case_1_actual = videoDownload.get_clean_unique_file_name(case_1_in, known_files)
        self.assertEqual(case_1_actual,case_1_exp)
        known_files.add(case_1_actual)

        case_2_actual = videoDownload.get_clean_unique_file_name(case_2_in, known_files)
        self.assertEqual(case_2_actual,case_2_exp)
        known_files.add(case_2_actual)

        case_3_actual = videoDownload.get_clean_unique_file_name(case_3_in, known_files)
        self.assertEqual(case_3_actual,case_3_exp)
        known_files.add(case_3_actual)

        case_4_actual = videoDownload.get_clean_unique_file_name(case_4_in, known_files)
        self.assertEqual(case_4_actual,case_4_exp)
        known_files.add(case_4_actual)

if __name__ == '__main__':
    unittest.main()
