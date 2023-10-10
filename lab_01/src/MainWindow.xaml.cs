using MathNet.Numerics.Distributions;
using OxyPlot.Series;
using OxyPlot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using ScottPlot;

namespace Distribution
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void PlotUniform(object sender, RoutedEventArgs e)
        {
            try
            {
                double a = Convert.ToDouble(LeftBorder.Text);
                double b = Convert.ToDouble(RightBorder.Text);

                double xl = a - 1.0;
                double xr = b + 1.0;

                double step = (xr - xl) / 900;

                List<double> xList = new();
                List<double> yFunctionList = new();
                List<double> yDensityList = new();

                var uniform = new ContinuousUniform(a, b);

                while (xl <= xr)
                {
                    xList.Add(xl);
                    yFunctionList.Add(uniform.CumulativeDistribution(xl));
                    yDensityList.Add(uniform.Density(xl));

                    xl += step;
                }

                Function.Reset();
                Density.Reset();

                Function.Plot.AddScatter(xList.ToArray(), yFunctionList.ToArray(), color: System.Drawing.Color.Blue, markerSize: 2);
                Density.Plot.AddScatter(xList.ToArray(), yDensityList.ToArray(), color: System.Drawing.Color.Brown, markerSize: 2);

                Function.Refresh();
                Density.Refresh();
            }
            catch (ArgumentException)
            {
                MessageBox.Show("Ошибка: левая граница должна быть меньше правой.");
            }
            catch (FormatException)
            {
                MessageBox.Show("Ошибка: параметры должны быть вещественными числами.");
            }
        }

        private void PlotErlang(object sender, RoutedEventArgs e)
        {
            try
            {
                int shape = Convert.ToInt32(Shape.Text);
                double rate = Convert.ToDouble(Rate.Text);

                double xl = 0.0;
                double xr = 20.0;

                double step = (xr - xl) / 900;

                List<double> xList = new();
                List<double> yFunctionList = new();
                List<double> yDensityList = new();

                var erlang = new Erlang(shape, rate);

                while (xl <= xr)
                {
                    xList.Add(xl);
                    yFunctionList.Add(erlang.CumulativeDistribution(xl));
                    yDensityList.Add(erlang.Density(xl));

                    xl += step;
                }

                Function.Reset();
                Density.Reset();

                Function.Plot.AddScatter(xList.ToArray(), yFunctionList.ToArray(), color: System.Drawing.Color.Red, markerSize: 2);
                Density.Plot.AddScatter(xList.ToArray(), yDensityList.ToArray(), color: System.Drawing.Color.Green, markerSize: 2);

                Function.Refresh();
                Density.Refresh();
            }
            catch (ArgumentException)
            {
                MessageBox.Show("Ошибка: форма должна быть целым положительным числом.");
            }
            catch (FormatException)
            {
                MessageBox.Show("Ошибка: параметры должны быть вещественными числами.");
            }
        }
    }
}
