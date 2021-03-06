# Copyright 1999-2020 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd

import mars.dataframe as md
from mars.tests.core import TestBase, ExecutorForTest


class Test(TestBase):
    def setUp(self):
        super().setUp()
        self.executor = ExecutorForTest()

    def testSetIndex(self):
        df1 = pd.DataFrame([[1, 3, 3], [4, 2, 6], [7, 8, 9]],
                           index=['a1', 'a2', 'a3'], columns=['x', 'y', 'z'])
        df2 = md.DataFrame(df1, chunk_size=2)

        expected = df1.set_index('y', drop=True)
        df3 = df2.set_index('y', drop=True)
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df3, concat=True)[0])

        expected = df1.set_index('y', drop=False)
        df4 = df2.set_index('y', drop=False)
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df4, concat=True)[0])

    def testILocGetItem(self):
        df1 = pd.DataFrame([[1, 3, 3], [4, 2, 6], [7, 8, 9]],
                           index=['a1', 'a2', 'a3'], columns=['x', 'y', 'z'])
        df2 = md.DataFrame(df1, chunk_size=2)

        # plain index
        expected = df1.iloc[1]
        df3 = df2.iloc[1]
        pd.testing.assert_series_equal(
            expected, self.executor.execute_dataframe(df3, concat=True)[0])

        # plain index on axis 1
        expected = df1.iloc[:2, 1]
        df4 = df2.iloc[:2, 1]
        pd.testing.assert_series_equal(
            expected, self.executor.execute_dataframe(df4, concat=True)[0])

        # slice index
        expected = df1.iloc[:, 2:4]
        df5 = df2.iloc[:, 2:4]
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df5, concat=True)[0])

        # plain fancy index
        expected = df1.iloc[[0], [0, 1, 2]]
        df6 = df2.iloc[[0], [0, 1, 2]]
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df6, concat=True)[0])

        # plain fancy index with shuffled order
        expected = df1.iloc[[0], [1, 2, 0]]
        df7 = df2.iloc[[0], [1, 2, 0]]
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df7, concat=True)[0])

        # fancy index
        expected = df1.iloc[[1, 2], [0, 1, 2]]
        df8 = df2.iloc[[1, 2], [0, 1, 2]]
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df8, concat=True)[0])

        # fancy index with shuffled order
        expected = df1.iloc[[2, 1], [1, 2, 0]]
        df9 = df2.iloc[[2, 1], [1, 2, 0]]
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df9, concat=True)[0])

        # one fancy index
        expected = df1.iloc[[2, 1]]
        df10 = df2.iloc[[2, 1]]
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df10, concat=True)[0])

        # plain index
        expected = df1.iloc[1, 2]
        df11 = df2.iloc[1, 2]
        self.assertEqual(
            expected, self.executor.execute_dataframe(df11, concat=True)[0])

        # bool index array
        expected = df1.iloc[[True, False, True], [2, 1]]
        df12 = df2.iloc[[True, False, True], [2, 1]]
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df12, concat=True)[0])

        # bool index
        expected = df1.iloc[[True, False, True], [2, 1]]
        df13 = df2.iloc[md.Series([True, False, True], chunk_size=1), [2, 1]]
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df13, concat=True)[0])

        # test Series
        data = pd.Series(np.arange(10))
        series = md.Series(data, chunk_size=3).iloc[:3]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data.iloc[:3])

        series = md.Series(data, chunk_size=3).iloc[4]
        self.assertEqual(
            self.executor.execute_dataframe(series, concat=True)[0], data.iloc[4])

        series = md.Series(data, chunk_size=3).iloc[[2, 3, 4, 9]]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data.iloc[[2, 3, 4, 9]])

        series = md.Series(data, chunk_size=3).iloc[[4, 3, 9, 2]]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data.iloc[[4, 3, 9, 2]])

        series = md.Series(data).iloc[5:]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data.iloc[5:])

        # bool index array
        selection = np.random.RandomState(0).randint(2, size=10, dtype=bool)
        series = md.Series(data).iloc[selection]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data.iloc[selection])

        # bool index
        series = md.Series(data).iloc[md.Series(selection, chunk_size=4)]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data.iloc[selection])

    def testILocSetItem(self):
        df1 = pd.DataFrame([[1, 3, 3], [4, 2, 6], [7, 8, 9]],
                           index=['a1', 'a2', 'a3'], columns=['x', 'y', 'z'])
        df2 = md.DataFrame(df1, chunk_size=2)

        # plain index
        expected = df1
        expected.iloc[1] = 100
        df2.iloc[1] = 100
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df2, concat=True)[0])

        # slice index
        expected.iloc[:, 2:4] = 1111
        df2.iloc[:, 2:4] = 1111
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df2, concat=True)[0])

        # plain fancy index
        expected.iloc[[0], [0, 1, 2]] = 2222
        df2.iloc[[0], [0, 1, 2]] = 2222
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df2, concat=True)[0])

        # fancy index
        expected.iloc[[1, 2], [0, 1, 2]] = 3333
        df2.iloc[[1, 2], [0, 1, 2]] = 3333
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df2, concat=True)[0])

        # plain index
        expected.iloc[1, 2] = 4444
        df2.iloc[1, 2] = 4444
        pd.testing.assert_frame_equal(
            expected, self.executor.execute_dataframe(df2, concat=True)[0])

        # test Series
        data = pd.Series(np.arange(10))
        series = md.Series(data, chunk_size=3)
        series.iloc[:3] = 1
        data.iloc[:3] = 1
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data)

        series.iloc[4] = 2
        data.iloc[4] = 2
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data)

        series.iloc[[2, 3, 4, 9]] = 3
        data.iloc[[2, 3, 4, 9]] = 3
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data)

        series.iloc[5:] = 4
        data.iloc[5:] = 4
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series, concat=True)[0], data)

    def testLocGetItem(self):
        rs = np.random.RandomState(0)
        # index and columns are labels
        raw1 = pd.DataFrame(rs.randint(10, size=(5, 4)),
                            index=['a1', 'a2', 'a3', 'a4', 'a5'],
                            columns=['a', 'b', 'c', 'd'])
        # columns are labels
        raw2 = raw1.copy()
        raw2.reset_index(inplace=True, drop=True)
        # columns are non unique and monotonic
        raw3 = raw1.copy()
        raw3.columns = ['a', 'b', 'b', 'd']
        # columns are non unique and non monotonic
        raw4 = raw1.copy()
        raw4.columns = ['b', 'a', 'b', 'd']

        df1 = md.DataFrame(raw1, chunk_size=2)
        df2 = md.DataFrame(raw2, chunk_size=2)
        df3 = md.DataFrame(raw3, chunk_size=2)
        df4 = md.DataFrame(raw4, chunk_size=2)

        df = df2.loc[3, 'b']
        result = self.executor.execute_tensor(df, concat=True)[0]
        expected = raw2.loc[3, 'b']
        self.assertEqual(result, expected)

        df = df1.loc['a3', 'b']
        result = self.executor.execute_tensor(df, concat=True)[0]
        expected = raw1.loc['a3', 'b']
        self.assertEqual(result, expected)

        df = df2.loc[1:4, 'b':'d']
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw2.loc[1:4, 'b': 'd']
        pd.testing.assert_frame_equal(result, expected)

        df = df2.loc[:4, 'b':]
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw2.loc[:4, 'b':]
        pd.testing.assert_frame_equal(result, expected)

        # slice on axis index whose index_value does not have value
        df = df1.loc['a2':'a4', 'b':]
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw1.loc['a2':'a4', 'b':]
        pd.testing.assert_frame_equal(result, expected)

        df = df2.loc[:, 'b']
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw2.loc[:, 'b']
        pd.testing.assert_series_equal(result, expected)

        # 'b' is non-unique
        df = df3.loc[:, 'b']
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw3.loc[:, 'b']
        pd.testing.assert_frame_equal(result, expected)

        # 'b' is non-unique, and non-monotonic
        df = df4.loc[:, 'b']
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw4.loc[:, 'b']
        pd.testing.assert_frame_equal(result, expected)

        # label on axis 0
        df = df1.loc['a2', :]
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw1.loc['a2', :]
        pd.testing.assert_series_equal(result, expected)

        # label-based fancy index
        df = df2.loc[[3, 0, 1], ['c', 'a', 'd']]
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw2.loc[[3, 0, 1], ['c', 'a', 'd']]
        pd.testing.assert_frame_equal(result, expected)

        # label-based fancy index, asc sorted
        df = df2.loc[[0, 1, 3], ['a', 'c', 'd']]
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw2.loc[[0, 1, 3], ['a', 'c', 'd']]
        pd.testing.assert_frame_equal(result, expected)

        # label-based fancy index in which non-unique exists
        selection = rs.randint(2, size=(5,), dtype=bool)
        df = df3.loc[selection, ['b', 'a', 'd']]
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw3.loc[selection, ['b', 'a', 'd']]
        pd.testing.assert_frame_equal(result, expected)

        df = df3.loc[md.Series(selection), ['b', 'a', 'd']]
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw3.loc[selection, ['b', 'a', 'd']]
        pd.testing.assert_frame_equal(result, expected)

        # label-based fancy index on index
        # whose index_value does not have value
        df = df1.loc[['a3', 'a1'], ['b', 'a', 'd']]
        result = self.executor.execute_dataframe(df, concat=True)[0]
        expected = raw1.loc[['a3', 'a1'], ['b', 'a', 'd']]
        pd.testing.assert_frame_equal(result, expected)

    def testDataFrameGetitem(self):
        data = pd.DataFrame(np.random.rand(10, 5), columns=['c1', 'c2', 'c3', 'c4', 'c5'])
        df = md.DataFrame(data, chunk_size=2)

        series1 = df['c2']
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series1, concat=True)[0], data['c2'])

        series2 = df['c5']
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series2, concat=True)[0], data['c5'])

        df1 = df[['c1', 'c2', 'c3']]
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df1, concat=True)[0], data[['c1', 'c2', 'c3']])

        df2 = df[['c3', 'c2', 'c1']]
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df2, concat=True)[0], data[['c3', 'c2', 'c1']])

        df3 = df[['c1']]
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df3, concat=True)[0], data[['c1']])

        df4 = df[['c3', 'c1', 'c2', 'c1']]
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df4, concat=True)[0], data[['c3', 'c1', 'c2', 'c1']])

        df5 = df[np.array(['c1', 'c2', 'c3'])]
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df5, concat=True)[0], data[['c1', 'c2', 'c3']])

        df6 = df[['c3', 'c2', 'c1']]
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df6, concat=True)[0], data[['c3', 'c2', 'c1']])

        df7 = df[1:7:2]
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df7, concat=True)[0], data[1:7:2])

        series3 = df['c1'][0]
        self.assertEqual(
            self.executor.execute_dataframe(series3, concat=True)[0], data['c1'][0])

    def testDataFrameGetitemBool(self):
        data = pd.DataFrame(np.random.rand(10, 5), columns=['c1', 'c2', 'c3', 'c4', 'c5'])
        df = md.DataFrame(data, chunk_size=2)

        mask_data = data.c1 > 0.5
        mask = md.Series(mask_data, chunk_size=2)

        # getitem by mars series
        self.assertEqual(
            self.executor.execute_dataframe(df[mask], concat=True)[0].shape, data[mask_data].shape)
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df[mask], concat=True)[0], data[mask_data])

        # getitem by pandas series
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df[mask_data], concat=True)[0], data[mask_data])

        # getitem by mars series with alignment but no shuffle
        mask_data = pd.Series([True, True, True, False, False, True, True, False, False, True],
                              index=range(9, -1, -1))
        mask = md.Series(mask_data, chunk_size=2)
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df[mask], concat=True)[0], data[mask_data])

        # getitem by mars series with shuffle alignment
        mask_data = pd.Series([True, True, True, False, False, True, True, False, False, True],
                              index=[0, 3, 6, 2, 9, 8, 5, 7, 1, 4])
        mask = md.Series(mask_data, chunk_size=2)
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df[mask], concat=True)[0].sort_index(), data[mask_data])

        # getitem by mars series with shuffle alignment and extra element
        mask_data = pd.Series([True, True, True, False, False, True, True, False, False, True, False],
                              index=[0, 3, 6, 2, 9, 8, 5, 7, 1, 4, 10])
        mask = md.Series(mask_data, chunk_size=2)
        pd.testing.assert_frame_equal(
            self.executor.execute_dataframe(df[mask], concat=True)[0].sort_index(), data[mask_data])

    def testDataFrameGetitemUsingAttr(self):
        data = pd.DataFrame(np.random.rand(10, 5), columns=['c1', 'c2', 'key', 'dtypes', 'size'])
        df = md.DataFrame(data, chunk_size=2)

        series1 = df.c2
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series1, concat=True)[0], data.c2)

        # accessing column using attribute shouldn't overwrite existing attributes
        self.assertEqual(df.key, getattr(getattr(df, '_data'), '_key'))
        self.assertEqual(df.size, data.size)
        pd.testing.assert_series_equal(df.dtypes, data.dtypes)

        # accessing non-existing attributes should trigger exception
        with self.assertRaises(AttributeError):
            _ = df.zzz  # noqa: F841

    def testSeriesGetitem(self):
        data = pd.Series(np.random.rand(10))
        series = md.Series(data)
        self.assertEqual(
            self.executor.execute_dataframe(series[1], concat=True)[0], data[1])

        data = pd.Series(np.random.rand(10), name='a')
        series = md.Series(data, chunk_size=4)

        for i in range(10):
            series1 = series[i]
            self.assertEqual(
                self.executor.execute_dataframe(series1, concat=True)[0], data[i])

        series2 = series[[0, 1, 2, 3, 4]]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series2, concat=True)[0], data[[0, 1, 2, 3, 4]])

        series3 = series[[4, 3, 2, 1, 0]]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series3, concat=True)[0], data[[4, 3, 2, 1, 0]])

        series4 = series[[1, 2, 3, 2, 1, 0]]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series4, concat=True)[0], data[[1, 2, 3, 2, 1, 0]])
        #
        index = ['i' + str(i) for i in range(20)]
        data = pd.Series(np.random.rand(20), index=index, name='a')
        series = md.Series(data, chunk_size=3)

        for idx in index:
            series1 = series[idx]
            self.assertEqual(
                self.executor.execute_dataframe(series1, concat=True)[0], data[idx])

        selected = ['i1', 'i2', 'i3', 'i4', 'i5']
        series2 = series[selected]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series2, concat=True)[0], data[selected])

        selected = ['i4', 'i7', 'i0', 'i1', 'i5']
        series3 = series[selected]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series3, concat=True)[0], data[selected])

        selected = ['i0', 'i1', 'i5', 'i4', 'i0', 'i1']
        series4 = series[selected]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series4, concat=True)[0], data[selected])

        selected = ['i0']
        series5 = series[selected]
        pd.testing.assert_series_equal(
            self.executor.execute_dataframe(series5, concat=True)[0], data[selected])
