import { Component, OnInit } from '@angular/core';
import * as Highcharts from 'highcharts';
import { Options } from 'highcharts';
import { HttpClient } from '@angular/common/http';


// Define an interface for a single record
interface SensorRecord {
  temperature: number;
  humidity: number;
  moisture: number;
  lux: number;
  pH: number;
  minute: string;
}

@Component({
  selector: 'app-line-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.css'],
})
export class LineChartComponent implements OnInit {

  averageData: any; // Store average data here
  latestData: any;  // Store latest data here

  //-----------------------------------------------------------
  //declare temperature chart
  //-----------------------------------------------------------
  Highcharts: typeof Highcharts = Highcharts;
  chartOptions: Highcharts.Options = {
    title: {
      text: 'Temperature Chart',
    },
    xAxis: {
      type: 'datetime',
    },
    yAxis: {
      title: {
        text: 'temperature'
      },
    },
    plotOptions:{
      line:{
        dataLabels:{
          enabled:true
        }
      }
    },
    series: [
      {
        type: 'line',
        name: 'Time',
        data: [], // Start with an empty data array
      },
    ],
  };
  chart: Highcharts.Chart | undefined; // Declare chart reference

  //-----------------------------------------------------------
  //declare humidity chart
  //-----------------------------------------------------------
  Highcharts_humidity: typeof Highcharts = Highcharts;
  chartOptions_humidity: Highcharts.Options = {
    title: {
      text: 'Humidity Chart',
    },
    xAxis: {
      type: 'datetime',
    },
    yAxis: {
      title: {
        text: 'humidity'
      },
    },
    plotOptions:{
      line:{
        dataLabels:{
          enabled:true
        }
      }
    },
    series: [
      {
        type: 'line',
        name: 'Time',
        data: [], // Start with an empty data array
      },
    ],
  };
  chart_humidity: Highcharts.Chart | undefined; // Declare chart reference

 //-----------------------------------------------------------
  //declare moisture chart
//-----------------------------------------------------------
  Highcharts_moisture: typeof Highcharts = Highcharts;
  chartOptions_moisture: Highcharts.Options = {
    title: {
      text: 'Moisture Chart',
    },
    xAxis: {
      type: 'datetime',
    },
    yAxis: {
      title: {
        text: 'moisture'
      },
    },
    plotOptions:{
      line:{
        dataLabels:{
          enabled:true
        }
      }
    },
    series: [
      {
        type: 'line',
        name: 'Time',
        data: [], // Start with an empty data array
      },
    ],
  };
  chart_moisture: Highcharts.Chart | undefined; // Declare chart reference


  //-----------------------------------------------------------
  //declare lux chart
  //-----------------------------------------------------------
  Highcharts_lux: typeof Highcharts = Highcharts;
  chartOptions_lux: Highcharts.Options = {
    title: {
      text: 'Lux Chart',
    },
    xAxis: {
      type: 'datetime',
    },
    yAxis: {
      title: {
        text: 'lux'
      },
    },
    plotOptions:{
      line:{
        dataLabels:{
          enabled:true
        }
      }
    },
    series: [
      {
        type: 'line',
        name: 'Time',
        data: [], // Start with an empty data array
      },
    ],
  };
  chart_lux: Highcharts.Chart | undefined; // Declare chart reference

// ----------------------------------------------------------------------------
 //-----------------------------------------------------------
  //declare pH chart
  //-----------------------------------------------------------
  Highcharts_pH: typeof Highcharts = Highcharts;
  chartOptions_pH: Highcharts.Options = {
    title: {
      text: 'PH Chart',
    },
    xAxis: {
      type: 'datetime',
    },
    yAxis: {
      title: {
        text: 'pH'
      },
    },
    plotOptions:{
      line:{
        dataLabels:{
          enabled:true
        }
      }
    },
    series: [
      {
        type: 'line',
        name: 'Time',
        data: [], // Start with an empty data array
      },
    ],
  };
  chart_pH: Highcharts.Chart | undefined; // Declare chart reference

// ----------------------------------------------------------------------------
// -----------------------------------------------------------------------------
  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    
    //average of last day
    //average of last week
    this.averageValues();

    // Create the chart instance
    this.chart = Highcharts.chart('chart-container', this.chartOptions);  // temperature
    this.chart_humidity = Highcharts.chart('chart-container-humidity', this.chartOptions_humidity);
    this.chart_moisture = Highcharts.chart('chart-container-moisture', this.chartOptions_moisture);   
    this.chart_lux = Highcharts.chart('chart-container-lux', this.chartOptions_lux);
    this.chart_pH = Highcharts.chart('chart-container-pH', this.chartOptions_pH);

    this.liveRecordsSensorsAPICall(); //to call api first time and get historical values

    setInterval(() => {

     this.averageValues();
     this.liveRecordsSensorsAPICall();  //call after every 20 second  
    }, 20000); // 60000 milliseconds = 1 minute
  }


  //get average values from python api for average values
  averageValues(): void{
    const apiUrl = "http://localhost:8000/latestSensorData";
    const headers = {
      "Content-Type": "application/json"
    };
    this.http.get(apiUrl, { headers }).subscribe(
      (response: any) => {
        console.log("API response", response);

        this.averageData = response.average;
        this.latestData = response.latest;




      });
  };

  //get live values from python api for live records
  liveRecordsSensorsAPICall(): void {
    const apiUrl = "http://localhost:8000/liveRecordsSensorData";
    const headers = {
      "Content-Type": "application/json"
    };
  
    this.http.get(apiUrl, { headers }).subscribe(
      (response: any) => {
        console.log("API response", response);
  
        console.log(response.liveRecords[0]);
  
        const liveRecords: SensorRecord[] = response.liveRecords;
  
        const chart = this.chart; // Store this.chart in a local variable
  
        if (chart) {

          liveRecords.forEach(record => {
            const timestamp = new Date(record.minute).getTime();
            
            const temperature = record.temperature;
            
            
            console.log(temperature);
            console.log(timestamp);


            // Add temperature data to the chart's first series
            if (chart.series[0]) {
              chart.series[0].addPoint([timestamp, temperature]);
            }
            else{
              console.log("no series for temperature");
            }
  

          });
        }
        else{
          console.log("no temperature chart");
        }

        //---------------------------------------------------------------------------
        //Humidity chart
        //---------------------------------------------------------------------------
        const chart_humidity = this.chart_humidity; // Store this.chart in a local variable
        if (chart_humidity) {

          liveRecords.forEach(record => {
            const timestamp = new Date(record.minute).getTime();
            
            
            const humidity = record.humidity;
            
            console.log(timestamp);


            // Add temperature data to the chart's first series
            if (chart_humidity.series[0]) {
              chart_humidity.series[0].addPoint([timestamp, humidity]);
            }
            else{
              console.log("no series for humidity");
            }
  

          });
        }
        else{
          console.log("no humidity chart");
        }
        //---------------------------------------------------------------------------
        //moisture chart
        //---------------------------------------------------------------------------
        const chart_moisture = this.chart_moisture; // Store this.chart in a local variable
        if (chart_moisture) {

          liveRecords.forEach(record => {
            const timestamp = new Date(record.minute).getTime();
            
            
            const moisture = record.moisture;
            
            console.log(timestamp);


            // Add temperature data to the chart's first series
            if (chart_moisture.series[0]) {
              chart_moisture.series[0].addPoint([timestamp, moisture]);
            }
            else{
              console.log("no series for moisture");
            }
  

          });
        }
        else{
          console.log("no moisture chart");
        }
          //---------------------------------------------------------------------------
        //lux chart
        //---------------------------------------------------------------------------
        const chart_lux= this.chart_lux; // Store this.chart in a local variable
        if (chart_lux) {

          liveRecords.forEach(record => {
            const timestamp = new Date(record.minute).getTime();
            
            
            const lux = record.lux;
            
            console.log(timestamp);


            // Add temperature data to the chart's first series
            if (chart_lux.series[0]) {
              chart_lux.series[0].addPoint([timestamp, lux]);
            }
            else{
              console.log("no series for moisture");
            }
  

          });
        }
        else{
          console.log("no moisture chart");
        }
        //---------------------------------------------------------------------------
        //pH chart
        //---------------------------------------------------------------------------
        const chart_pH = this.chart_pH; // Store this.chart in a local variable
        if (chart_pH) {

          liveRecords.forEach(record => {
            const timestamp = new Date(record.minute).getTime();
            
            
            const pH = record.pH;
            
            console.log(timestamp);


            // Add temperature data to the chart's first series
            if (chart_pH.series[0]) {
              chart_pH.series[0].addPoint([timestamp, pH]);
            }
            else{
              console.log("no series for moisture");
            }
  

          });
        }
        else{
          console.log("no moisture chart");
        }
//-------------------------------------------------------------------------------------------------------- 
        /// display current value in one div

      },
      (error) => {
        console.log("API error", error);
      }
    );


  }
  
  
}
