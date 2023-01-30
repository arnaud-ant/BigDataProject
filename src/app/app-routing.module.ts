import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { QuestionPanelComponent } from './question-panel/question-panel.component';
import { QuizzComponent } from './quizz/quizz.component';

const routes: Routes = [
  {path: '', component: LoginComponent},
  {path:'home', component:HomeComponent},
  {path:'quizz/:id', component:QuizzComponent},
  {path:'analytics', component:HomeComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
