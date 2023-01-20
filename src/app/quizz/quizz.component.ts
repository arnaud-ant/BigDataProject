import { sanitizeIdentifier } from '@angular/compiler';
import {  HostListener,Component } from '@angular/core';
import { Question } from '../service/question';
import { Router } from '@angular/router';


@Component({
  selector: 'app-quizz',
  templateUrl: './quizz.component.html',
  styleUrls: ['./quizz.component.css']
})
export class QuizzComponent {

  @HostListener('document:keyup', ['$event'])
  async handleKeyboardEvent(event: KeyboardEvent) {
    if (event.key == ' ' && !this.recordVoice ) {
      this.recordVoice=true;
      console.log('enter pressed')
      setTimeout(()=>{ this.recordVoice = false }, 5000)
    }
  }

  constructor(private _router: Router){}

  questions=[
    {
      index:1,
      label:"La tour Eiffel est la plus haute structure de Paris ?",
      answer:[{answer:"oui",valid:true},{answer:"non",valid:false},{answer:"peut etre",valid:false},{answer:"nsp",valid:false}]
    },
    {
      index:2,
      label:"L’apparition de traces blanches à la surface du chocolat est causée par la fermentation du sucre ?",
      answer:[{answer:"oui",valid:true},{answer:"non",valid:false},{answer:"peut etre",valid:false},{answer:"nsp",valid:false}]
    },
    {
      index:3,
      label:"Quelle est l'énergie renouvelable la plus utilisée ?",
      answer:[{answer:"hydro",valid:true},{answer:"eolien",valid:false},{answer:"solaire",valid:false},{answer:"geothermie",valid:false}]
    },
    {
      index:4,
      label:"L'alcool a-t-il été interdit aux joueurs de pétanque professionnels en 2007 ?",
      answer:[{answer:"oui",valid:true},{answer:"non",valid:false},{answer:"peut etre",valid:false},{answer:"nsp",valid:false}]
    },
    {
      index:5,
      label:"Quelle est la particularité des fourmis légionnaires ?",
      answer:[{answer:"8pattes",valid:true},{answer:"Cannibales",valid:false},{answer:"Végétariennes",valid:false},{answer:"Aveugles",valid:false}]
    },
    {
      index:6,
      label:"En combien de langues est proposé Wikipédia ?",
      answer:[{answer:"1150",valid:true},{answer:"2300",valid:false},{answer:"3420",valid:false},{answer:"4500",valid:false}]
    },
    {
      index:7,
      label:"La construction du mur de Berlin a commencé en 1951 ?",
      answer:[{answer:"oui",valid:true},{answer:"non",valid:false},{answer:"peut etre",valid:false},{answer:"nsp",valid:false}]
    },
    {
      index:8,
      label:"Le jeu vidéo Among Us est sorti en 2018 ?",
      answer:[{answer:"oui",valid:true},{answer:"non",valid:false},{answer:"peut etre",valid:false},{answer:"nsp",valid:false}]
    },
    {
      index:9,
      label:"Il y a plus de grains de sable sur Terre que d’étoiles dans l’univers ?",
      answer:[{answer:"oui",valid:true},{answer:"non",valid:false},{answer:"peut etre",valid:false},{answer:"nsp",valid:false}]
    },
    {
      index:10,
      label:"Dans la série Les Simpsons, quel est le deuxième prénom de Milhouse Van Houten ?",
      answer:[{answer:"Adolf",valid:true},{answer:"Staline ",valid:false},{answer:"Mussolini",valid:false},{answer:"Franco",valid:false}]
    },
  ]


currentQuestionId:number=1;
currentQuestion:Question = this.questions[this.currentQuestionId-1];
score:number=0;
recordVoice:boolean=false;

getNextQuestion(){
  
  this.currentQuestionId++;

  if(this.currentQuestionId > 10){
    const message = 'terminé ! votre socre est de : ' + this.score + '/' + this.questions.length;
    alert(message);
    this._router.navigateByUrl('/home');
  }else{
    console.log("going to next question")
    this.currentQuestion = this.questions[this.currentQuestionId-1];
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
