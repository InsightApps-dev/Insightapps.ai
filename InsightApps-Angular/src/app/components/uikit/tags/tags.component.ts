import { Component, inject } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { MaterialModuleModule } from '../../../material-module/material-module.module';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { MatChipInputEvent, MatChipEditedEvent } from '@angular/material/chips';
import { TagInputModule } from 'ngx-chips';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
export interface tag {
  name: string;
}
@Component({
  selector: 'app-tags',
  standalone: true,
  imports: [SharedModule,NgbModule,MaterialModuleModule,TagInputModule,FormsModule,ReactiveFormsModule],
  templateUrl: './tags.component.html',
  styleUrls: ['./tags.component.scss']
})
export class TagsComponent {
  handleCardClick(event:Event): void {
    // Prevent the click event from propagating to the container
    // event.preventDefault();
    event.stopPropagation();
  }
 
removeRow(rowId: string) {
  const rowElement = document.getElementById(rowId);
  if (rowElement) {
    rowElement.remove();
  }
}
}
