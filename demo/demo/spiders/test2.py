import matplotlib.pyplot as plt
import pandas as pd
def grafico():
        # Create a sample data
        data = {'date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05'],
                'price': [100, 120, 90, 110, 130]}
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['price'], '-o', markersize=8, linewidth=2)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Historical Price Chart')

        # Save the chart as a JPEG image
        plt.savefig('historical_price_chart.jpg')
