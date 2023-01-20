import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Question } from '../service/question';

@Component({
  selector: 'app-question-panel',
  templateUrl: './question-panel.component.html',
  styleUrls: ['./question-panel.component.css']
})
export class QuestionPanelComponent {
  @Input()
  question!: Question;

  @Output() childEvent = new EventEmitter();
returnAnswer(index:number){
  this.childEvent.emit(index);
}

  
}
