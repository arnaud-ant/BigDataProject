import { Component } from '@angular/core';
import { faSignIn, faHouse, faBarChart } from '@fortawesome/free-solid-svg-icons';
import { totalScore } from '../global-variables';

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
  

  analyticsHover:boolean = false;
  homeHover:boolean = false;

  ngOnInit()  {
    for (let index = 0; index < this.taille; index++) {
      this.addition+=this.total.at(index);
    }
    this.moyenne=this.addition/this.taille
  }

}
