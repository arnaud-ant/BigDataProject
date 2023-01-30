import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {AwsLambdaService} from '../service/aws-service.service';
import { faSignIn, faHouse, faBarChart } from '@fortawesome/free-solid-svg-icons';
import { GlobalVar } from '../global-variables'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  constructor(private _router: Router,private lambdaService: AwsLambdaService){
    if(GlobalVar.connectedUser.username == ""){
      this._router.navigateByUrl('/');
    }
  }

  public fullResponse!: AWS.Lambda.InvocationResponse;
  public lambdaResponse: any;
  lambdaName: string = "getQuizz";
  lambdares:boolean=false;
  faSignIn=faSignIn;
  faHouse=faHouse;
  faBarChart=faBarChart;

  analyticsHover:boolean = false;
  homeHover:boolean = false;


  startQuizz(id:number){
    this._router.navigateByUrl('/quizz/' + id);
  }
}
