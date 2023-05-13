import unittest
import sortParseDown
from parseChannels import MetaData

class SPDTest(unittest.TestCase):
    '''
        Tests all of the helper functions in sortParseDown
    '''
    def test_load_channels(self):
        '''
            Tests load_channels
        '''
        expected_channels = ["test1", "test2", "test3", "test4", "test5", "test6"]
        actual_channels = sortParseDown.load_channels("test.csv")
        self.assertEqual(len(expected_channels), len(actual_channels))
        for channel in expected_channels:
            self.assertIn(channel, actual_channels)

    def test_is_unique_stream(self):
        '''
            Tests is_unique_stream
        '''
        def create_simple_metadata(channel, time_passed):
            return MetaData("link", "title", "length", 0, time_passed, channel)
        mdata_list = [create_simple_metadata("channel" + str(i), str(i) + " days ago") for i in range(1, 4)]

        self.assertTrue(sortParseDown.is_unique_stream(
            create_simple_metadata("channel1", "2 days ago"),
            mdata_list
        ))
        self.assertTrue(sortParseDown.is_unique_stream(
            create_simple_metadata("channel2", "1 days ago"),
            mdata_list
        ))
        self.assertFalse(sortParseDown.is_unique_stream(
            create_simple_metadata("channel3", "3 days ago"),
            mdata_list
        ))


    # def test_get_best_videos(self):
    #     '''
    #         Tests is_unique_stream
    #     '''
    #     pass

if __name__ == '__main__':
    unittest.main()
