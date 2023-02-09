import {  HostListener,Component } from '@angular/core';
import { formatDate } from '@angular/common'
import { Question } from '../service/question';
import { ActivatedRoute, Router } from '@angular/router';
import {AwsLambdaService} from '../service/aws-service.service';
import { GlobalVar } from '../global-variables';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-quizz',
  templateUrl: './quizz.component.html',
  styleUrls: ['./quizz.component.css']
})
export class QuizzComponent {



  constructor(private _router: Router, private lambdaService: AwsLambdaService,private route: ActivatedRoute){

    if(GlobalVar.connectedUser.username == ""){
      this._router.navigateByUrl('/');
    }else{
      this.route.params.subscribe( params => this.quizzId = params['id']);
      console.log('loading quizz n°',this.quizzId)
      this.getQuizz(+this.quizzId-1);
    }

    
  }

quizzId:number=0;
questions:Question[]=[]
currentQuestionId:number=1;
currentQuestion:Question = this.questions[this.currentQuestionId-1];
score:number=0;
recordVoice:boolean=false;

public fullResponse!: AWS.Lambda.InvocationResponse;
public lambdaResponse: any;
lambdaName: string = "lambda-srapping";
lambdares:boolean=false;

public async getQuizz(quizzId:number){
  let request = {
    id: quizzId
  };
  //invoke lambda from the lambda service
  let response = await this.lambdaService.invokeLambda(this.lambdaName, request);
  
  //parse the response data from our function
  if(response){
    this.fullResponse = response;
    let res = JSON.parse(response?.Payload?.toString()?? "");
    console.log(res);
    this.processQuestions(res.questions,res.reponses,res.valeurs);
    this.currentQuestionId=1;
    this.currentQuestion = this.questions[this.currentQuestionId-1];
    this.lambdaResponse = res;
    console.log(this.lambdaResponse);
    console.log(this.questions)
    console.log(this.lambdaResponse.questions)
  }
  
}

processQuestions(questionlist:string,answerlist:string,resultlist:string){
  let questionArray=JSON.parse(questionlist);
  let answerArray=JSON.parse(answerlist);
  let resultArray=JSON.parse(resultlist);
  let i;
  for (i=0; i<questionArray.length; i++) {
   let q = {
    index:i,
    label:questionArray[i],
    answer:[{answer:answerArray[i*4],valid:resultArray[i*4]},{answer:answerArray[i*4+1],valid:resultArray[i*4+1]},{answer:answerArray[i*4+2],valid:resultArray[i*4+2]},{answer:answerArray[i*4+3],valid:resultArray[i*4+3]}]
  }
  this.questions.push(q)
 }
}

getNextQuestion(){
  
  this.currentQuestionId++;

  if(this.currentQuestionId > 10){
    const message =   'Votre socre est de : ' + this.score + '/10';
    this.sendScore(this.score);
    Swal.fire(
      'Terminé !',
      message,
      'success'
    )
    this._router.navigateByUrl('/home');
  }else{
    console.log("going to next question")
    this.currentQuestion = this.questions[this.currentQuestionId-1];
  }
}

public async sendScore(score:number){
  let lambdaName: string = "lambda-post-statistics";
  let request = {
    user_id:GlobalVar.connectedUser.id,
    quizz_id:this.quizzId,
    date: formatDate(new Date(), 'yyyy-MM-dd', 'en'),
    score:score,
  };
  //invoke lambda from the lambda service
  console.log(request);
  let response = await this.lambdaService.invokeLambda(lambdaName, request);
  
  //parse the response data from our function
  if(response){
    let res = JSON.parse(response?.Payload?.toString()?? "");
    this.lambdaResponse = res;
    console.log(this.lambdaResponse);
    let data = JSON.parse(this.lambdaResponse.body);
    console.log(data);
  }
}

checkAnswer(msg: any){
  console.log('la réponse ' + msg);
  if(this.currentQuestion?.answer[msg].valid){
    console.log("bonne réponse")
    this.score++;
  }else{
    console.log("perdu")
  }
  this.getNextQuestion();
}


}
