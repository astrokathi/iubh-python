import unittest

from task.exceptions.errors import ObjectNoneError
from task.loaddata import LoadData


class TestLoadData(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLoadData, self).__init__(*args, **kwargs)
        self.load_data = LoadData()

    def test_load_train_data(self):
        """
        ####################UNIT TEST#############################
        Unit test to determine whether the training data is loaded?
        :return:
        """
        self.assertIsNotNone(obj=self.load_data.load_train_data())

    def test_load_train_data_wrong_path(self):
        """
        ####################UNIT TEST#############################
        Unit test to raise a File not found exception for any given random path, here exception is handled so returns
        None
        :return:
        """
        train_data = self.load_data.load_train_data(file_path="/random")
        self.assertIsNone(train_data)

    def test_add_train_data_to_database_without_obj(self):
        """
        ####################UNIT TEST#############################
        Unit test to raise a ObjectNoneError in case of train object is None,
        It raises a custom exception and the scenario is tested here
        :return:
        """
        with self.assertRaises(ObjectNoneError):
            self.load_data.add_train_data_to_database()


if __name__ == "__main__":
    print("Running Load data unit tests started")
    unittest.main()
    print("Running Load data unit tests ended")
