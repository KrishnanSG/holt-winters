import pandas as pd

class TimeSeries:
    """
    This a class for time series related operation on a TimeSeries dataset.

    Attributes
    ----------
    data  : pandas DataFrame
        Raw data.
    train : pandas DataFrame
        Data to be used for training the model.
    test  : pandas DataFrame
        Data used for test phase.
    """
    def __init__(self,filename,train_size=0.7):
        """
        The constructor for TimeSeries class. It loads and splits the dataset as per the given ratio.

        Generally the dataset for time series is of the format:
        date        values
        yyyy-mm-dd     x

        params
        ------
        train_size: float
            Value used to split the dataset into train and test data.
        """
        self.data = pd.read_csv(filename)
        self.data.rename(columns={1:'date',2:'values'})
        self.data['date'] = pd.to_datetime(self.data['date'])

        # set index and modify inplace without creating new object
        self.data.set_index(self.data['date'],inplace=True)

        if train_size>1 or train_size<0:
            raise Exception("Invalid train_size, should be a float between 0.0 and 1.0")

        no_of_rows_in_dataset = self.data.shape[0]
        split_index = int(no_of_rows_in_dataset*train_size)
        self.train = self.data.iloc[:split_index,1]
        self.test = self.data.iloc[split_index-1:,1]

    def set_scale(self,factor=1):
        """Scales values in the time series"""
        self.train/=factor
        self.test/=factor
