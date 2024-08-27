import { ApexAxisChartSeries, ApexChart, ApexDataLabels, ApexPlotOptions, ApexYAxis, ApexXAxis, ApexFill, ApexTooltip, ApexStroke, ApexResponsive, ChartType, ApexLegend, ApexGrid } from "ng-apexcharts";

export type ChartOptions = {
    series: ApexAxisChartSeries;
    chart: ApexChart;
    dataLabels: ApexDataLabels;
    plotOptions: ApexPlotOptions;
    yaxis: ApexYAxis;
    xaxis: ApexXAxis;
    fill: ApexFill;
    tooltip: ApexTooltip;
    stroke: ApexStroke;
    grid:ApexGrid;
    colors:string[];
    responsive: ApexResponsive[]
    // legend: ApexLegend;
  };
  
export interface DONUT {
 series:number[];
  colors:string[];
  chart:{
    // events:any
  type: ChartType;
  height: number;
  // Other properties specific to the chart
}
legend:ApexLegend
dataLabels:{
enabled:boolean
},
labels:string[]
responsive:[{
  breakpoint:number;
  options:{
      chart:{
          width:number
      },
      legend:{
          show:boolean;
         
      },

      
  }
}]
stroke: {
  show: boolean,
  width: number,
  colors: string[],
}
}
  
  export const chartOptions:ChartOptions = {
    series: [
        {
            name: 'Online',
            data: [44, 55, 57, 56, 61, 58, 63, 60, 66],
            color:'rgb(21,58,84)'
          },
          {
            name: "Offline",
            data: [76, 85, 101, 98, 87, 105, 91, 114, 94],
          },
          {
            name: "Marketing",
            data: [35, 41, 36, 26, 45, 48, 52, 53, 41],
          },
    ],
    colors: ["rgb(21, 58, 84)", "rgb(0, 165, 162)", "rgb(166, 142, 94)"],
    chart: {
      type: "bar",
      height: 355
    },
    grid: {
      show: true,
      borderColor: "rgba(119, 119, 142, 0.1)",
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "55%",
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      show: true,
      width: 3,
      colors: ["transparent"]
    },
    xaxis: {
      categories: ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"],
      labels: {
        show: true,
        style: {
          colors: "#8c9097",
          fontSize: "11px",
          fontWeight: 600,
          cssClass: "apexcharts-xaxis-label",
        },
      },
      axisBorder: {
        show: true,
        color: "rgba(119, 119, 142, 0.05)",
        offsetX: 0,
        offsetY: 0,
      },
      axisTicks: {
        show: true,
        borderType: "solid",
        color: "rgba(119, 119, 142, 0.05)",
        offsetX: 0,
        offsetY: 0,
      },
    },
    yaxis: {
      // title: {
      //   text: "$ (thousands)"
      // }
    },
    fill: {
      opacity: 1
    },
    tooltip: {
      y: {
        formatter: function(val) {
          return "$ " + val + " thousands";
        }
      }
    },
    
    responsive: [
      {
        breakpoint: 768,
        options: {
          plotOptions: {
            bar: {
              columnWidth: '70%', // Adjust column width for smaller screens
            }
          }
        }
      }
    ],
  };
  export const  chartOptions4:any = {
    series: [
      {
        data: [34, 55, 41, 47, 32, 43, 31],
         color:'rgb(46,144,143)',
      },
    ],
    chart: {
      sparkline: {
        enabled: true,
      },
      dropShadow: {
        enabled: true,
        enabledOnSeries: undefined,
        top: 3,
        right: 6,
        blur: 3,
        opacity: 0.2,
      },
      type: 'line',
      height: 60,
      width: 80,
    },
    tooltip: {
      x: {
        show: false,
      },
      y: {
        title: {
          formatter: function () {
            return '';
          },
        },
      },
      marker: {
        show: false,
      },
    },
   
    stroke: {
      width: [1.5],
      curve: ['smooth'],
    },
    xaxis: {
      crosshairs: {
        show: false,
      },
    },
    fill: {
      type: 'gradient',
      gradient: {
        opacityFrom: 0.9,
        opacityTo: 0.9,
        stops: [0, 98],
      },
    },
  };
  export const  chartOptions3:any = {
    series: [
      {
        data: [25, 39, 36, 47, 32, 43, 31],
        color:'rgb(215,110,116)',
      },
    ],
    chart: {
      sparkline: {
        enabled: true,
      },
      dropShadow: {
        enabled: true,
        enabledOnSeries: undefined,
        top: 3,
        right: 6,
        blur: 3,
        opacity: 0.2,
      },
      type: 'line',
      height: 60,
      width: 80,
    },
    tooltip: {
      x: {
        show: false,
      },
      y: {
        title: {
          formatter: function () {
            return '';
          },
        },
      },
      marker: {
        show: false,
      },
    },
   
    stroke: {
      width: [1.5],
      curve: ['smooth'],
    },
    xaxis: {
      crosshairs: {
        show: false,
      },
    },
    fill: {
      type: 'gradient',
      gradient: {
        opacityFrom: 0.9,
        opacityTo: 0.9,
        stops: [0, 98],
      },
    },
  };
  export const  chartOptions5:any = {
    series: [
      {
        name: 'Revenue',
        data: [55,  52, 55, 52, 55, 55, 58,58, 53,  55, 54,55],
        color: 'rgb(46,144,143)',
      },
    ],
    chart: {
      height: 123,
      type: 'area',
      sparkline: {
        enabled: true,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      width: [1.4],
      show: true,
      curve: ['smooth'],
    },
    xaxis: {
      crosshairs: {
        show: false,
      },
    },
    legend: {
      show: false,
    },
    labels: [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
    ],
    markers: {
      size: 0,
    },
   
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.4,
        opacityTo: 0.7,
        stops: [0, 100],
      },
    },
  };
  export const DonutChartData:DONUT = {
    series: [44, 55, 33, 55, 33],
  labels: ["Accepted", "Rejected", "Dispatched", "Delivered", "Cancelled"],
  chart: {
  
    height: 250,
    type: "donut",
  },
  dataLabels: {
    enabled: false,
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: 220,
        },
        legend: {
          show: false,
        },
      },
    },
  ],
  colors: ["#00a5a2c9", "#17b1dfb0", "#f7b725bf", "#44b86cbf", "#be495fbd"],
  legend: {
    show: true,
    position: "right",
    markers: {
      width: 10,
      height: 10,
    },
  },
  stroke: {
    show: true,
    width: 4,
    colors: ["transparent"],
  },
};