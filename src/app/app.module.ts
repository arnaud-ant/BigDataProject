import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { QuestionPanelComponent } from './question-panel/question-panel.component';
import { HomeComponent } from './home/home.component';
import { QuizzComponent } from './quizz/quizz.component';
import { GraphComponent } from './graph/graph.component';
import { GoogleChartsModule } from 'angular-google-charts';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    QuestionPanelComponent,
    HomeComponent,
    QuizzComponent,
    GraphComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    FontAwesomeModule,
    GoogleChartsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
