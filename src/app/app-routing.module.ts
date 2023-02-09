import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GraphComponent } from './graph/graph.component';
import { AnalyticsComponent } from './analytics/analytics.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { QuestionPanelComponent } from './question-panel/question-panel.component';
import { QuizzComponent } from './quizz/quizz.component';

const routes: Routes = [
  {path: '', component: LoginComponent},
  {path:'home', component:HomeComponent},
  {path:'quizz/:id', component:QuizzComponent},
  {path:'analytics', component:HomeComponent},
  {path:'chart', component:GraphComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
