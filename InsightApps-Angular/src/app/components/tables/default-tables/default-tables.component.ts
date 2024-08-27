import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';

@Component({
  selector: 'app-default-tables',
  standalone: true,
  imports: [SharedModule],
  templateUrl: './default-tables.component.html',
  styleUrl: './default-tables.component.scss'
})
export class DefaultTablesComponent {

}
