import math

import numpy as np


class table:
    """
    The class table contains data and methods for printing a latex table.
    """

    def __init__(self, file_name):
        """
        The constructor of the class.

        Parameters:
            file_name (str): Name of the file where the table will be printed.
        """
        self.file_name = file_name
        self.columns = []
        self.column_names = []
        self.column_units = []
        self.column_format = []
        self.column_separator = ' & '
        self.row_separator = ' \\\\'
        self.table_start = '\\begin{tabular}'
        self.table_end = '\\end{tabular}'
        self.table_caption = ''
        self.table_label = ''
        self.empty_field_symbol = '-'

    def is_integers(self, nums):
        return np.all(np.mod(nums, 1) == 0)
    
    def round_to_significant_figures(self, arr, n):
        """
        Rounds all numbers in a NumPy array to n significant figures.
        
        Parameters:
            arr (numpy.ndarray): Input array of numbers.
            n (int): Number of significant figures.
            
        Returns:
            numpy.ndarray: Array with numbers rounded to n significant figures.
        """
        if n <= 0:
            raise ValueError("Number of significant figures must be positive.")
        
        # Handle the array magnitude to determine scaling
        abs_arr = np.abs(arr)  # Absolute values
        orders = np.where(abs_arr > 0, np.floor(np.log10(abs_arr)), 0)  # Order of magnitude
        scale_factors = np.power(10, -orders + (n - 1))
        
        # Scale, round, and rescale the array
        rounded = np.round(arr * scale_factors) / scale_factors
        
        return rounded

    def add_column(self, values, name, unit='', format='c', n_digits=None, n_significant=None, n_blank_fields=0):
        """
        Individual columns are added with the add_column method.

        Parameters:
            values (list or numpy.ndarray): List of values in the column.
            name (str): Name of the column.
            unit (str): Unit of the values in the column.
            format (str): Format of the column (default is 'c').
            n_digits (int): For rounding. Numbers of digits after the decimal point.
            n_significant (int): Another rounding option. Number of significant figures.
            n_blank_fields (int): Number of empty fields at the beginning of the column.
        """
        self.column_names.append(name)
        self.column_units.append(f'\\texttt{{[{unit}]}}' if unit else unit)
        self.column_format.append(format)

        # Convert values to np.array.
        values = np.array(values)

        # Put the blank fields at the beginning of the column.
        column = [self.empty_field_symbol] * n_blank_fields

        # Preprocess values.
        print(values)
        if n_significant:
            values = self.round_to_significant_figures(values, n_significant)
        print(values)

        # If n_digits is specified, round the values to n_digits after the decimal point and padd with empty spaces.
        # Check the highest order of magnitude of the values.
        # Note that it is the number x from 10^x.
        orders = np.zeros_like(values)  # Initialize with zeros
        nonzero_mask = values != 0      # Mask for non-zero values
        orders[nonzero_mask] = np.floor(np.log10(np.abs(values[nonzero_mask])))
        # Convert the orders to integers.
        orders = orders.astype(int)
        max_order = max(orders)

        # Calculate the number of digits before the decimal point.
        n_tot = 0
        if max_order >= 0:
            n_tot += max_order + 1 + 1  # One for the sign.

        if self.is_integers(values):
            n_digits = 0
        else:
            n_tot += 1  # Decimal point.
            if n_digits:
                n_tot += n_digits
            else:
                n_digits = len(str(min(abs(values))).split('.')[1])
                n_tot += n_digits

        # column += [f'{val:{n_tot}.{n_digits}f}' for val in values]
        column += [f'{val:{n_tot}.{n_digits}f}' for val in values]

        self.columns.append(column)

    def print_table(self):
        """
        The print_table method prints the table in latex format.
        """
        with open(self.file_name, 'w') as f:
            f.write(self.table_start + '{' + ''.join(self.column_format) + '}\n')
            f.write('\\hline\n')
            f.write(self.column_separator.join(self.column_names) + self.row_separator + '\n')

            # If there is at least one unit, print the units in the next row
            if any(self.column_units):
                f.write(self.column_separator.join(self.column_units) + self.row_separator + '\n')
            f.write('\\hline\n')

            # Print the numbers.
            for i in range(len(self.columns[0])):
                row = []
                for j in range(len(self.columns)):
                    try:
                        row.append(self.columns[j][i])
                    except IndexError:
                        row.append(self.empty_field_symbol)
                f.write(self.column_separator.join(row) + self.row_separator + '\n')
            f.write('\\hline\n')

            # Print the caption and label.
            if self.table_caption:
                f.write('\\caption{' + self.table_caption + '}\n')
            if self.table_label:
                f.write('\\label{' + self.table_label + '}\n')
            f.write(self.table_end + '\n')

if __name__ == '__main__':
    t = table('table_output.tex')
    t.add_column([10, 20, 30]         , 'U', 'V', 'c', n_digits=0)
    t.add_column([0.114, 0.206, 0.317], 'I', 'A', 'c', n_digits=2)
    t.print_table()
