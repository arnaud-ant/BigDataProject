import { Component } from '@angular/core';
import { ChartType, Row } from "angular-google-charts";

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent {


  title = 'Google Chart Example';
  type = ChartType.ColumnChart;

  columnsChartdata = [
    ['[12/12/22]', 10, 'color: rgb(255, 166, 0)', 'Quizz 1'],
    ['[13/12/22]', 3, 'color: rgb(255, 166, 0)', 'Quizz 7'],
    ['[13/12/22]', 2, 'color: rgb(255, 166, 0)', 'Quizz 2'],
    ['[16/12/22]', 5, 'color: rgb(255, 166, 0)', 'Quizz 3'],
    ['[17/12/22]', 9, 'color: rgb(255, 166, 0)', 'Quizz 3'],
    ['[12/12/22]', 10, 'color: rgb(255, 166, 0)', 'Quizz 1'],
    ['[13/12/22]', 3, 'color: rgb(255, 166, 0)', 'Quizz 7'],
    ['[13/12/22]', 2, 'color: rgb(255, 166, 0)', 'Quizz 2'],
    ['[16/12/22]', 5, 'color: rgb(255, 166, 0)', 'Quizz 3'],
    ['[17/12/22]', 9, 'color: rgb(255, 166, 0)', 'Quizz 3'],
  ];
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
    fontSize: 9,
    legend: 'dsd',
  };
}
