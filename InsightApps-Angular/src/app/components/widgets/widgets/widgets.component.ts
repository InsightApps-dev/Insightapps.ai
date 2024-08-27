import { Component, HostListener } from '@angular/core';
import { latLng, tileLayer, Map } from 'leaflet';
import { RouterModule } from '@angular/router';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';
import {  chartOptions3, chartOptions4, chartOptions5 } from '../../../shared/data/dashboard';
import * as chartData  from '../../../shared/data/widgets';
import { chartOptions } from '../../../shared/data/widgets';
import { NgApexchartsModule } from 'ng-apexcharts';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';


import {
  CdkDragDrop,
  CdkDrag,
  CdkDropList,
  CdkDropListGroup,
  moveItemInArray,
  transferArrayItem,
} from '@angular/cdk/drag-drop';
@Component({
  selector: 'app-widgets',
  standalone:true,
  imports: [RouterModule,LeafletModule,NgApexchartsModule,SharedModule,NgbModule,CdkDropListGroup, CdkDropList, CdkDrag],
  templateUrl: './widgets.component.html',
  styleUrls: ['./widgets.component.scss']
})
export class WidgetsComponent {

  todo = ['Get to work', 'Pick up groceries', 'Go home', 'Fall asleep'];

  done = ['Get up', 'Brush teeth', 'Take a shower', 'Check e-mail', 'Walk dog'];

  drop(event: CdkDragDrop<string[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex,
      );
    }
  }









































 /* public chartOptions5 = chartOptions5;
  public chartOptions3 = chartOptions3;
  public chartOptions4 = chartOptions4;
  public echartLineBarOption:Partial<any> = chartData.echartLineBarOption;
  public chartOptions = chartOptions;
  public generateData(
    baseval: number,
    count: number,
    yrange: { min: number; max: number }
  ) {
    let i = 0;
    const series = [];
    while (i < count) {
      const x = Math.floor(Math.random() * (750 - 1 + 1)) + 1;
      const y =
        Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
      const z = Math.floor(Math.random() * (75 - 15 + 1)) + 15;

      series.push([x, y, z]);
      baseval += 86400000;
      i++;
    }
    return series;
  }
  center = latLng([46.879966, -121.726909]);
  options = {
    layers: [
      tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: 'Open Street Map',
      }),
    ],
    zoom: 5,
    center: latLng(this.center),
  };

  get width() {
    return window.innerWidth;
  }

  @HostListener('resize')
  onMapReady(map: Map) {
    setTimeout(() => map.invalidateSize(), 1);
  }
  scroll(el: HTMLElement) {
    el.scrollIntoView({ behavior: 'smooth' });
  }
  
  scrolled = false;*/
}
