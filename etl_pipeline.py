import pandas as pd


class Base:
    def wrangle(self, file_path):
        """
        This method is to read in the csv file and clean it for better
        usability in Tableau. It saves the cleaned data frame back into a csv
        file locally.
        """
        # Reads in the data into a pandas data frame.
        data = pd.read_csv(file_path)
        # These are the wanted columns from the data frame.
        df = data[['place', 'submitted_date',
                    'primary_time_seconds', 'real_time_seconds', 'player_name',
                    'player_country', 'platform', 'verified']]

        clean_df = self.date_fixer(self.time_checker(df))
        clean_df.fillna('Unspecified', inplace=True)
        print("Data Cleaned!!!")
        clean_df.to_csv('cleaned_data.csv', index=False)

        # except:
        #     print(f"Fix this -> {self.time_checker(df)}")

    @staticmethod
    def time_checker(df):
        """
        This function is to check if there is a difference between the two time
        columns. This is to check before dropping the primary time column. It
        runs a list comprehension and to identify the placement, it uses the
        index plus one. This is because placements start at 1st place.

        If any two column cells don't match, they will be placed into the list
        and individually printed out into the console with their respective
        index.
        """
        place_list = [
            placement + 1 for placement, (pts, rts) in
            enumerate(zip(df['primary_time_seconds'], df['real_time_seconds']))
            if pts != rts
        ]

        # Returns either the list of non-matches or the cleaned df.
        if place_list:
            for placement in place_list:
                print(
                    f"""
                    At placement {placement}, index {placement-1}, the
                    primary and real time seconds are different.
                    """
                    )
            return place_list
        else:
            return df.drop(columns="primary_time_seconds", axis=1)

    @staticmethod
    def date_fixer(test_df):
        """
        Using list comprehension, this function pulls the date and arranges
        into m/d/y format for better readability while also removing the
        seconds from the submission. If the value is null, its added to the
        list as is. The list replaces the input data frame and then returned.
        """
        test_df.submitted_date = [
            date[5:10].replace("-", "/") + "/" + date[:4]
            if pd.isna(date) is False else date
            for date in test_df['submitted_date']
        ]
        return test_df

if __name__ == '__main__':
    c = Base()
    c.wrangle(
        r"C:/Users/Owner\Documents/Projects/application/SM64 Runs/data_120 Star.csv"
        )