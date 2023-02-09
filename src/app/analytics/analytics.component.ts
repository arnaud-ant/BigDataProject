import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { faSignIn, faHouse, faBarChart } from '@fortawesome/free-solid-svg-icons';
import { ChartType } from 'angular-google-charts';
import { GlobalVar, totalScore } from '../global-variables';
import { AwsLambdaService } from '../service/aws-service.service';

@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.css']
})
export class AnalyticsComponent {
  total = totalScore;
  taille = totalScore.length;
  addition=0;
  moyenne=0;

  faSignIn=faSignIn;
  faHouse=faHouse;
  faBarChart=faBarChart;

  scores:any[]=[];
  chartData:any[]=[];
  averageScore:number=0.0;
  analyticsHover:boolean = false;
  homeHover:boolean = false;

  constructor(private _router: Router,private lambdaService: AwsLambdaService){}

  ngOnInit()  {
    if(GlobalVar.connectedUser.username == ""){
      this._router.navigateByUrl('/');
    }
    
    this.loadScores();
  }


  public lambdaResponse: any;
  lambdares:boolean=false;

  public async loadScores(){
    let lambdaName: string = "lambda-get-statistics-by-user";
    let request = {
      id:GlobalVar.connectedUser.id
    };
    //invoke lambda from the lambda service
    let response = await this.lambdaService.invokeLambda(lambdaName, request);
    
    //parse the response data from our function
    if(response){
      let res = JSON.parse(response?.Payload?.toString()?? "");
      this.lambdaResponse = res;
      console.log(this.lambdaResponse);
      let data = JSON.parse(this.lambdaResponse.body);
      console.log(data);
      if(data == "No statistics for this user"){
        console.log('No statistics for this user')
      }else{
        this.scores=data;
        this.loadChartData();
        this.chartData = Object.assign([],this.chartData);
        this.scores.forEach((value:any,index:any) =>{
          this.averageScore += value[4];
        });
        this.averageScore = this.averageScore/this.scores.length;
      }
    }
  }

 
  loadChartData(){
    this.scores.forEach((value: any,index: any) => {
      this.chartData.push([value[3], value[4], 'color: rgb(255, 166, 0)', 'Quizz '+value[2]])
    });

  }

  title = 'Google Chart Example';
  type = ChartType.ColumnChart;

  columnsChartdatacolumn = [
    'Date',
    'Score',
    { role: 'style' },
    { role: 'annotation' },
  ];
  columnsChartoptions = {
    title: '',
    tooltip: {
      textStyle: { color: 'blue', fontName: 'Tahoma', fontSize: '15' },
    },
    labels: 'none',
    is3D: false ,
    static:false,
    fontSize: 9,
    legend: 'dsd',
  };

}
