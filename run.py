#!/usr/bin/env python

import pandas as pd

# read csv
base_data = pd.read_csv('./clang_master_release.csv')
unroll_data = pd.read_csv('./clang_unroll_release.csv')


bms = ['bm', 'dhrystone', 'coremark']
# order by time consuming
unroll_data.sort_values('time_consume', ascending=False)

# create sub-dataframe for each module
for m in bms:
	sub_unroll_df = unroll_data[unroll_data.module==m]

# rename a column
sub_unroll_df.rename(columns = {'time_consume':'unroll_time_consume'}, inplace=True)
sub_base_df.rename(columns = {'time_consume':'base_time_consume'}, inplace=True)

# merge two table into one
sub_df = pd.merge(sub_base_df,sub_unroll_df, on=['module', 'source_file'])

# drop a column
sub_df.drop(['module'], axis=1, inplace=True)

# assign a new column
inc_ratio = (sub_df.unroll_time_consume - sub_df.base_time_consume)/sub_df.base_time_consume
sub_df = sub_df.assign(inc_ratio = inc_ratio)


# optional: Display as percentage
sub_df['inc_ratio'] = pd.Series(["{0:.2f}%".format(val * 100) for val in sub_df['inc_ratio']], index = sub_df.index)


# plot and save as image
ax = sub_df.plot(x=sub_df.source_file, kind='bar')
fig = ax.get_figure()
fig.savefig('./foo.png')