import { Component } from '@angular/core';
import { series } from './data';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgApexchartsModule } from 'ng-apexcharts';

@Component({
  selector: 'app-apexcharts',
  standalone: true,
  imports: [SharedModule,NgApexchartsModule],
  templateUrl: './apexcharts.component.html',
  styleUrls: ['./apexcharts.component.scss']
})
export class ApexchartsComponent {
  chartOptions:any;
  chartOptions1:any;
  chartOptions2:any;
  chartOptions3:any;
  chartOptions4:any;
  chartOptions5:any;
  chartOptions6:any;
  chartOptions7:any;
  chartOptions8:any;
  chartOptions9:any;
  chartOptions10:any;
  chartOptions11:any;
  chartOptions12:any;
  chartOptions13:any;
  chartOptions14:any;
  chartOptions15:any;
  chartOptions16:any;
  chartOptions17:any;
  constructor(){
    this.chartOptions={
        series: [{
            name: "Desktops",
            data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
        }],
       
            chart: {
                height: 320,
                type: 'line',
                reponsive: true,
                zoom: {
                    enabled: false
                },
                events: {
                    mounted: (chart:any) => {
                      chart.windowResizeHandler();
                    }
                  },
            },
            colors: ['#00a5a2'],
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'straight',
                width: 3,
            },
            grid: {
              borderColor: "rgba(119, 119, 142, 0.05)",
            },
            title: {
                text: 'Product Trends by Month',
                align: 'left',
                style: {
                    fontSize: '13px',
                    fontWeight: 'bold',
                    color: '#8c9097'
                },
            },
            xaxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
                labels: {
                    show: true,
                    style: {
                        colors: "#8c9097",
                        fontSize: '11px',
                        fontWeight: 600,
                        cssClass: 'apexcharts-xaxis-label',
                    },
                }
            },
            yaxis: {
                labels: {
                    show: true,
                    style: {
                        colors: "#8c9097",
                        fontSize: '11px',
                        fontWeight: 600,
                        cssClass: 'apexcharts-yaxis-label',
                    },
                }
            }
        
    }
    this.chartOptions1 = {
      series: [
        {
          name: "STOCK ABC",
          data: series.monthDataSeries1.prices,
        },
      ],
      chart: {
        type: "area",
        height: 320,
        zoom: {
          enabled: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        curve: "straight",
      },
      subtitle: {
        text: "Price Movements",
        align: "left",
        style: {
          fontSize: "11px",
          fontWeight: "normal",
          color: "#8c9097",
        },
      },
      grid: {
        borderColor: "rgba(119, 119, 142, 0.05)",
      },
      labels: series.monthDataSeries1.dates,
      title: {
        text: "Fundamental Analysis of Stocks",
        align: "left",
        style: {
          fontSize: "13px",
          fontWeight: "bold",
          color: "#8c9097",
        },
      },
      colors: ["#00a5a2"],
      xaxis: {
        type: "datetime",
        labels: {
          show: true,
          style: {
            colors: "#8c9097",
            fontSize: "11px",
            fontWeight: 600,
            cssClass: "apexcharts-xaxis-label",
          },
        },
      },
      yaxis: {
        opposite: true,
        labels: {
          show: true,
          style: {
            colors: "#8c9097",
            fontSize: "11px",
            fontWeight: 600,
            cssClass: "apexcharts-xaxis-label",
          },
        },
      },
      legend: {
        horizontalAlign: "left",
      },
    };
    this.chartOptions2 = {
      series: [
        {
          name: 'Net Profit',
          data: [44, 55, 57, 56, 61, 58, 63, 60, 66],
        },
        {
          name: 'Revenue',
          data: [76, 85, 101, 98, 87, 105, 91, 114, 94],
        },
        {
          name: 'Free Cash Flow',
          data: [35, 41, 36, 26, 45, 48, 52, 53, 41],
        },
      ],
      colors:['#00a5a2','#0dc9c5','#f43f63'],
      chart: {
        type: 'bar',
        height: 320,
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          // endingShape: "rounded"
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent'],
      },
      xaxis: {
        categories: [
          'Feb',
          'Mar',
          'Apr',
          'May',
          'Jun',
          'Jul',
          'Aug',
          'Sep',
          'Oct',
        ],
      },
      yaxis: {
        title: {
          text: '$ (thousands)',
        },
      },
      fill: {
        opacity: 1,
      },
      tooltip: {
        y: {
          formatter: function (val: string) {
            return '$ ' + val + ' thousands';
          },
        },
      },
      grid: {
        borderColor: "rgba(119, 119, 142, 0.05)",
      },
    };
    this.chartOptions3 = {
      series: [
        {
          name: 'basic',
          data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380],
        },
      ],
      colors:['#00a5a2'],
      chart: {
        type: 'bar',
        height: 320,
      },
      plotOptions: {
        bar: {
          horizontal: true,
        },
      },
      dataLabels: {
        enabled: false,
      },
      xaxis: {
        categories: [
          'South Korea',
          'Canada',
          'United Kingdom',
          'Netherlands',
          'Italy',
          'France',
          'Japan',
          'United States',
          'China',
          'Germany',
        ],
      },
      grid: {
        borderColor: "rgba(119, 119, 142, 0.05)",
      }
    };
    this.chartOptions4 = {
      series: [
        {
          name: "Website Blog",
          type: "column",
          data: [440, 505, 414, 671, 227, 413, 201, 352, 752, 320, 257, 160]
        },
        {
          name: "Social Media",
          type: "line",
          data: [23, 42, 35, 27, 43, 22, 17, 31, 22, 22, 12, 16]
        }
      ],
      colors:['#00a5a2','#31d1ce'],
      chart: {
        height: 350,
        type: "line"
      },
      grid: {
        borderColor: "rgba(119, 119, 142, 0.05)",
      },
      stroke: {
        width: [0, 4]
      },
      title: {
        text: "Traffic Sources",
        style: {
          fontSize: "13px",
          fontWeight: "bold",
          color: "#8c9097",
        },
      },
      dataLabels: {
        enabled: true,
        enabledOnSeries: [1]
      },
      labels: [
        "01 Jan 2001",
        "02 Jan 2001",
        "03 Jan 2001",
        "04 Jan 2001",
        "05 Jan 2001",
        "06 Jan 2001",
        "07 Jan 2001",
        "08 Jan 2001",
        "09 Jan 2001",
        "10 Jan 2001",
        "11 Jan 2001",
        "12 Jan 2001"
      ],
      xaxis: {
        type: "datetime"
      },
      yaxis: [
        {
          title: {
            text: "Website Blog",
            style: {
              fontSize: "13px",
              fontWeight: "bold",
              color: "#8c9097",
            },
          }
        },
        {
          opposite: true,
          title: {
            text: "Social Media",
            style: {
              fontSize: "13px",
              fontWeight: "bold",
              color: "#8c9097",
            },
          }
        }
      ]
      
    };
    this.chartOptions5 = {
      series: [
        {
          data: [
            {
              x: "Code",
              y: [
                new Date("2019-03-02").getTime(),
                new Date("2019-03-04").getTime()
              ]
            },
            {
              x: "Test",
              y: [
                new Date("2019-03-04").getTime(),
                new Date("2019-03-08").getTime()
              ]
            },
            {
              x: "Validation",
              y: [
                new Date("2019-03-08").getTime(),
                new Date("2019-03-12").getTime()
              ]
            },
            {
              x: "Deployment",
              y: [
                new Date("2019-03-12").getTime(),
                new Date("2019-03-18").getTime()
              ]
            }
          ]
        }
      ],
      grid: {
        borderColor: "rgba(119, 119, 142, 0.05)",
      },
      colors:['#00a5a2'],
      chart: {
        height: 350,
        type: "rangeBar"
      },
      plotOptions: {
        bar: {
          horizontal: true
        }
      },
      xaxis: {
        type: "datetime"
      }
    };
    this.chartOptions6 = {
      series: [
        {
          name: "candle",
          data: [
            {
              x: new Date(1538778600000),
              y: [6629.81, 6650.5, 6623.04, 6633.33]
            },
            {
              x: new Date(1538780400000),
              y: [6632.01, 6643.59, 6620, 6630.11]
            },
            {
              x: new Date(1538782200000),
              y: [6630.71, 6648.95, 6623.34, 6635.65]
            },
            {
              x: new Date(1538784000000),
              y: [6635.65, 6651, 6629.67, 6638.24]
            },
            {
              x: new Date(1538785800000),
              y: [6638.24, 6640, 6620, 6624.47]
            },
            {
              x: new Date(1538787600000),
              y: [6624.53, 6636.03, 6621.68, 6624.31]
            },
            {
              x: new Date(1538789400000),
              y: [6624.61, 6632.2, 6617, 6626.02]
            },
            {
              x: new Date(1538791200000),
              y: [6627, 6627.62, 6584.22, 6603.02]
            },
            {
              x: new Date(1538793000000),
              y: [6605, 6608.03, 6598.95, 6604.01]
            },
            {
              x: new Date(1538794800000),
              y: [6604.5, 6614.4, 6602.26, 6608.02]
            },
            {
              x: new Date(1538796600000),
              y: [6608.02, 6610.68, 6601.99, 6608.91]
            },
            {
              x: new Date(1538798400000),
              y: [6608.91, 6618.99, 6608.01, 6612]
            },
            {
              x: new Date(1538800200000),
              y: [6612, 6615.13, 6605.09, 6612]
            },
            {
              x: new Date(1538802000000),
              y: [6612, 6624.12, 6608.43, 6622.95]
            },
            {
              x: new Date(1538803800000),
              y: [6623.91, 6623.91, 6615, 6615.67]
            },
            {
              x: new Date(1538805600000),
              y: [6618.69, 6618.74, 6610, 6610.4]
            },
            {
              x: new Date(1538807400000),
              y: [6611, 6622.78, 6610.4, 6614.9]
            },
            {
              x: new Date(1538809200000),
              y: [6614.9, 6626.2, 6613.33, 6623.45]
            },
            {
              x: new Date(1538811000000),
              y: [6623.48, 6627, 6618.38, 6620.35]
            },
            {
              x: new Date(1538812800000),
              y: [6619.43, 6620.35, 6610.05, 6615.53]
            },
            {
              x: new Date(1538814600000),
              y: [6615.53, 6617.93, 6610, 6615.19]
            },
            {
              x: new Date(1538816400000),
              y: [6615.19, 6621.6, 6608.2, 6620]
            },
            {
              x: new Date(1538818200000),
              y: [6619.54, 6625.17, 6614.15, 6620]
            },
            {
              x: new Date(1538820000000),
              y: [6620.33, 6634.15, 6617.24, 6624.61]
            },
            {
              x: new Date(1538821800000),
              y: [6625.95, 6626, 6611.66, 6617.58]
            },
            {
              x: new Date(1538823600000),
              y: [6619, 6625.97, 6595.27, 6598.86]
            },
            {
              x: new Date(1538825400000),
              y: [6598.86, 6598.88, 6570, 6587.16]
            },
            {
              x: new Date(1538827200000),
              y: [6588.86, 6600, 6580, 6593.4]
            },
            {
              x: new Date(1538829000000),
              y: [6593.99, 6598.89, 6585, 6587.81]
            },
            {
              x: new Date(1538830800000),
              y: [6587.81, 6592.73, 6567.14, 6578]
            },
            {
              x: new Date(1538832600000),
              y: [6578.35, 6581.72, 6567.39, 6579]
            },
            {
              x: new Date(1538834400000),
              y: [6579.38, 6580.92, 6566.77, 6575.96]
            },
            {
              x: new Date(1538836200000),
              y: [6575.96, 6589, 6571.77, 6588.92]
            },
            {
              x: new Date(1538838000000),
              y: [6588.92, 6594, 6577.55, 6589.22]
            },
            {
              x: new Date(1538839800000),
              y: [6589.3, 6598.89, 6589.1, 6596.08]
            },
            {
              x: new Date(1538841600000),
              y: [6597.5, 6600, 6588.39, 6596.25]
            },
            {
              x: new Date(1538843400000),
              y: [6598.03, 6600, 6588.73, 6595.97]
            },
            {
              x: new Date(1538845200000),
              y: [6595.97, 6602.01, 6588.17, 6602]
            },
            {
              x: new Date(1538847000000),
              y: [6602, 6607, 6596.51, 6599.95]
            },
            {
              x: new Date(1538848800000),
              y: [6600.63, 6601.21, 6590.39, 6591.02]
            },
            {
              x: new Date(1538850600000),
              y: [6591.02, 6603.08, 6591, 6591]
            },
            {
              x: new Date(1538852400000),
              y: [6591, 6601.32, 6585, 6592]
            },
            {
              x: new Date(1538854200000),
              y: [6593.13, 6596.01, 6590, 6593.34]
            },
            {
              x: new Date(1538856000000),
              y: [6593.34, 6604.76, 6582.63, 6593.86]
            },
            {
              x: new Date(1538857800000),
              y: [6593.86, 6604.28, 6586.57, 6600.01]
            },
            {
              x: new Date(1538859600000),
              y: [6601.81, 6603.21, 6592.78, 6596.25]
            },
            {
              x: new Date(1538861400000),
              y: [6596.25, 6604.2, 6590, 6602.99]
            },
            {
              x: new Date(1538863200000),
              y: [6602.99, 6606, 6584.99, 6587.81]
            },
            {
              x: new Date(1538865000000),
              y: [6587.81, 6595, 6583.27, 6591.96]
            },
            {
              x: new Date(1538866800000),
              y: [6591.97, 6596.07, 6585, 6588.39]
            },
            {
              x: new Date(1538868600000),
              y: [6587.6, 6598.21, 6587.6, 6594.27]
            },
            {
              x: new Date(1538870400000),
              y: [6596.44, 6601, 6590, 6596.55]
            },
            {
              x: new Date(1538872200000),
              y: [6598.91, 6605, 6596.61, 6600.02]
            },
            {
              x: new Date(1538874000000),
              y: [6600.55, 6605, 6589.14, 6593.01]
            },
            {
              x: new Date(1538875800000),
              y: [6593.15, 6605, 6592, 6603.06]
            },
            {
              x: new Date(1538877600000),
              y: [6603.07, 6604.5, 6599.09, 6603.89]
            },
            {
              x: new Date(1538879400000),
              y: [6604.44, 6604.44, 6600, 6603.5]
            },
            {
              x: new Date(1538881200000),
              y: [6603.5, 6603.99, 6597.5, 6603.86]
            },
            {
              x: new Date(1538883000000),
              y: [6603.85, 6605, 6600, 6604.07]
            },
            {
              x: new Date(1538884800000),
              y: [6604.98, 6606, 6604.07, 6606]
            }
          ]
        }
      ],
      grid: {
        borderColor: "rgba(119, 119, 142, 0.05)",
      },
      colors:[],
      chart: {
        type: "candlestick",
        height: 350
      },
      plotOptions: {
        candlestick: {
          colors: {
            upward: "rgb(0, 165, 162)",
            downward: "rgba(13, 201, 197, 1)"
          },
          wick: {
            useFillColor: true
          }
        }
      },
      title: {
        text: "CandleStick Chart",
        align: "left",
        style: {
          fontSize: "13px",
          fontWeight: "bold",
          color: "#8c9097",
        },
      },
      xaxis: {
        type: "datetime"
      },
      yaxis: {
        tooltip: {
          enabled: true
        }
      }
    };
    this.chartOptions7 = {
      series: [
        {
          type: "boxPlot",
          data: [
            {
              x: "Jan 2015",
              y: [54, 66, 69, 75, 88]
            },
            {
              x: "Jan 2016",
              y: [43, 65, 69, 76, 81]
            },
            {
              x: "Jan 2017",
              y: [31, 39, 45, 51, 59]
            },
            {
              x: "Jan 2018",
              y: [39, 46, 55, 65, 71]
            },
            {
              x: "Jan 2019",
              y: [29, 31, 35, 39, 44]
            },
            {
              x: "Jan 2020",
              y: [41, 49, 58, 61, 67]
            },
            {
              x: "Jan 2021",
              y: [54, 59, 66, 71, 88]
            }
          ]
        }
      ],
      grid: {
        borderColor: "rgba(119, 119, 142, 0.05)",
      },
      chart: {
        height: 350,
        type: "candlestick"
      },
      title: {
        text: "Basic BoxPlot Chart",
        align: "left",
        style: {
          fontSize: "13px",
          fontWeight: "bold",
          color: "#8c9097",
        },
      },
      plotOptions: {
        boxPlot: {
          colors: {
            upper: "#26b2b0",
            lower: "#31d1ce"
          }
        }
      }
    };
    this.chartOptions8 = {
      series: [
        {
          name: 'Product1',
          data: this.generateData(new Date('11 Feb 2017 GMT').getTime(), 20, {
            min: 10,
            max: 60,
          }),
        },
        {
          name: 'Product2',
          data: this.generateData(new Date('11 Feb 2017 GMT').getTime(), 20, {
            min: 10,
            max: 60,
          }),
        },
        {
          name: 'Product3',
          data: this.generateData(new Date('11 Feb 2017 GMT').getTime(), 20, {
            min: 10,
            max: 60,
          }),
        },
        {
          name: 'Product4',
          data: this.generateData(new Date('11 Feb 2017 GMT').getTime(), 20, {
            min: 10,
            max: 60,
          }),
        },
      ],
      grid: {
        borderColor: "rgba(119, 119, 142, 0.05)",
      },
      colors:['#65d3d0','#95dad9','#f9a3b4'],
      chart: {
        height: 350,
        type: 'bubble',
      },
      dataLabels: {
        enabled: false,
      },
      fill: {
        type: 'gradient',
      },
      title: {
        text: '3D Bubble Chart',
        style: {
          fontSize: "13px",
          fontWeight: "bold",
          color: "#8c9097",
        },
      },
      xaxis: {
        tickAmount: 12,
        type: 'datetime',
        labels: {
          rotate: 0,
        },
      },
      yaxis: {
        max: 70,
      },
      theme: {
        palette: 'palette2',
      },
    };
    this.chartOptions9 = {
      series: [
        {
          name: 'TEAM 1',
          data: this.generateDayWiseTimeSeries(
            new Date('11 Feb 2017 GMT').getTime(),
            20,
            {
              min: 10,
              max: 60,
            }
          ),
        },
        {
          name: 'TEAM 2',
          data: this.generateDayWiseTimeSeries(
            new Date('11 Feb 2017 GMT').getTime(),
            20,
            {
              min: 10,
              max: 60,
            }
          ),
        },
        {
          name: 'TEAM 3',
          data: this.generateDayWiseTimeSeries(
            new Date('11 Feb 2017 GMT').getTime(),
            30,
            {
              min: 10,
              max: 60,
            }
          ),
        },
        {
          name: 'TEAM 4',
          data: this.generateDayWiseTimeSeries(
            new Date('11 Feb 2017 GMT').getTime(),
            10,
            {
              min: 10,
              max: 60,
            }
          ),
        },
        {
          name: 'TEAM 5',
          data: this.generateDayWiseTimeSeries(
            new Date('11 Feb 2017 GMT').getTime(),
            30,
            {
              min: 10,
              max: 60,
            }
          ),
        },
      ],
   
      chart: {
        height: 350,
        type: 'scatter',
        zoom: {
          type: 'xy',
        },
      },
      dataLabels: {
        enabled: false,
      },
      grid: {
        borderColor: "rgba(119, 119, 142, 0.05)",
        xaxis: {
          lines: {
            show: true,
          },
        },
        yaxis: {
          lines: {
            show: true,
          },
        },
      },
      xaxis: {
        type: 'datetime',
      },
      yaxis: {
        max: 70,
      },
    };
    this.chartOptions10 = {
      series: [
        {
          name: 'Metric1',
          data: this.generateData1(18, {
            min: 0,
            max: 90,
          }),
        },
        {
          name: 'Metric2',
          data: this.generateData1(18, {
            min: 0,
            max: 90,
          }),
        },
        {
          name: 'Metric3',
          data: this.generateData1(18, {
            min: 0,
            max: 90,
          }),
        },
        {
          name: 'Metric4',
          data: this.generateData1(18, {
            min: 0,
            max: 90,
          }),
        },
        {
          name: 'Metric5',
          data: this.generateData1(18, {
            min: 0,
            max: 90,
          }),
        },
        {
          name: 'Metric6',
          data: this.generateData1(18, {
            min: 0,
            max: 90,
          }),
        },
        {
          name: 'Metric7',
          data: this.generateData1(18, {
            min: 0,
            max: 90,
          }),
        },
        {
          name: 'Metric8',
          data: this.generateData1(18, {
            min: 0,
            max: 90,
          }),
        },
        {
          name: 'Metric9',
          data: this.generateData1(18, {
            min: 0,
            max: 90,
          }),
        },
      ],
      chart: {
        height: 350,
        type: 'heatmap',
      },
      dataLabels: {
        enabled: false,
      },
      colors: ['#00a5a2'],
      title: {
        text: 'HeatMap Chart (Single color)',
        style: {
          fontSize: "13px",
          fontWeight: "bold",
          color: "#8c9097",
        },
      },
    };
    this.chartOptions11 = {
      series: [
        {
          data: [
            {
              x: 'New Delhi',
              y: 218,
            },
            {
              x: 'Kolkata',
              y: 149,
            },
            {
              x: 'Mumbai',
              y: 184,
            },
            {
              x: 'Ahmedabad',
              y: 55,
            },
            {
              x: 'Bangaluru',
              y: 84,
            },
            {
              x: 'Pune',
              y: 31,
            },
            {
              x: 'Chennai',
              y: 70,
            },
            {
              x: 'Jaipur',
              y: 30,
            },
            {
              x: 'Surat',
              y: 44,
            },
            {
              x: 'Hyderabad',
              y: 68,
            },
            {
              x: 'Lucknow',
              y: 28,
            },
            {
              x: 'Indore',
              y: 19,
            },
            {
              x: 'Kanpur',
              y: 29,
            },
          ],
        },
      ],
      colors: ["#00a5a2"],

      chart: {
        height: 350,
        type: 'treemap',
      },
      title: {
        text: 'Basic Treemap',
        style: {
          fontSize: "13px",
          fontWeight: "bold",
          color: "#8c9097",
        },
      },
    };
    this.chartOptions12={
      series: [44, 55, 13, 43, 22],
      chart: {
          height: 300,
          type: 'pie',
      },
      colors: ["#00a5a2", "#31d1ce", "#f5b849", "#49b6f5", "#e6533c"],
      labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
      legend: {
          position: "bottom"
      },
      dataLabels: {
          dropShadow: {
              enabled: false
          }
      },
      };
      this.chartOptions13={
        series: [44, 55, 41, 17, 15],
        chart: {
            type: 'donut',
            height: 290
        },
        legend: {
            position: 'bottom'
        },
        colors: ["#00a5a2", "#31d1ce", "#f5b849", "#49b6f5", "#e6533c"],
        dataLabels: {
            dropShadow: {
                enabled: false
            }
        },
      }
      this.chartOptions14= {
        series: [70],
        chart: {
            height: 290,
            type: 'radialBar',
        },
        colors: ["#00a5a2"],
        plotOptions: {
            radialBar: {
                hollow: {
                    size: '70%',
                }
            },
        },
        labels: ['Cricket'],
      };
      this.chartOptions15= {
        series: [67],
        chart: {
            height: 290,
            type: 'radialBar',
            offsetY: -10
        },
        colors: ["#00a5a2"],
        plotOptions: {
            radialBar: {
                startAngle: -135,
                endAngle: 135,
                dataLabels: {
                    name: {
                        fontSize: '16px',
                        offsetY: 120
                    },
                    value: {
                        offsetY: 76,
                        fontSize: '22px',
                        formatter: function (val: string) {
                            return val + "%";
                        }
                    }
                }
            }
        },
        fill: {
            type: 'gradient',
            gradient: {
                shade: 'dark',
                shadeIntensity: 0.15,
                inverseColors: false,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [0, 50, 65, 91]
            },
        },
        stroke: {
            dashArray: 4
        },
        labels: ['Median Ratio'],
      };
      this.chartOptions16= {
        series: [{
          name: 'Series 1',
          data: [80, 50, 30, 40, 100, 20],
      }, {
          name: 'Series 2',
          data: [20, 30, 40, 80, 20, 80],
      }, {
          name: 'Series 3',
          data: [44, 76, 78, 13, 43, 10],
      }],
      chart: {
          height: 320,
          type: 'radar',
          dropShadow: {
              enabled: true,
              blur: 1,
              left: 1,
              top: 1
          }
      },
      title: {
          text: 'Radar Chart - Multi Series',
          align: 'left',
          style: {
              fontSize: '13px',
              fontWeight: 'bold',
              color: '#8c9097'
          },
      },
      colors: ["#00a5a2", "#31d1ce", "#ed3d60"],
      stroke: {
          width: 2
      },
      fill: {
          opacity: 0.1
      },
      markers: {
          size: 0
      },
      xaxis: {
          categories: ['2011', '2012', '2013', '2014', '2015', '2016']
      }
        };
        this.chartOptions17 = {
          series: [14, 23, 21, 17, 15, 10, 12, 17, 21],
          chart: {
              type: 'polarArea',
              height: 360
          },
          stroke: {
              colors: ['#fff']
          },
          fill: {
              opacity: 0.8
          },
          legend: {
              position: 'bottom'
          },
          colors: ["#00a5a2", "#31d1ce", "#f5b849", "#49b6f5", "#e6533c", "#26bf94", "#a65e76", "#49b6f5", "#5b67c7"],
          responsive: [{
              breakpoint: 480,
              options: {
                  chart: {
                      width: 200
                  },
                  legend: {
                      position: 'bottom'
                  }
              }
          }]
        };
}

public generateData(
  baseval: number,
  count: number,
  yrange: { min: any; max: any }
) {
  var i = 0;
  var series = [];
  while (i < count) {
    var x = Math.floor(Math.random() * (750 - 1 + 1)) + 1;
    var y =
      Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
    var z = Math.floor(Math.random() * (75 - 15 + 1)) + 15;

    series.push([x, y, z]);
    baseval += 86400000;
    i++;
  }
  return series;
}
public generateDayWiseTimeSeries(
  baseval: number,
  count: number,
  yrange: { min: any; max: any }
) {
  var i = 0;
  var series = [];
  while (i < count) {
    var y =
      Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

    series.push([baseval, y]);
    baseval += 86400000;
    i++;
  }
  return series;
}
public generateData1(count: number, yrange: { min: any; max: any }) {
  var i = 0;
  var series = [];
  while (i < count) {
    var x = 'w' + (i + 1).toString();
    var y =
      Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

    series.push({
      x: x,
      y: y,
    });
    i++;
  }
  return series;
}
}