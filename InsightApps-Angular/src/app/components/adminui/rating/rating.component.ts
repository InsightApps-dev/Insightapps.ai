import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { BarRatingModule } from 'ngx-bar-rating';
import { FormsModule, ReactiveFormsModule, UntypedFormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-rating',
  standalone: true,
  imports: [SharedModule,NgbModule,FormsModule,ReactiveFormsModule],
  templateUrl: './rating.component.html',
  styleUrls: ['./rating.component.scss']
})
export class RatingComponent {
  squareRate = 3;
  faRate = 3;
  currentRate = 5;
  customCurrentRate = 5;
  customCurrentRateInput = 5;
  selected = 0;
  selected1 = 0;
  selected2 = 0;
  hovered = 0;
  hovered1 = 0;
  readonly = false;
  heartRate = 3.45;
  ctrl: UntypedFormControl;
  ctrl1: UntypedFormControl;
  constructor() {
    this.ctrl = new UntypedFormControl(null, Validators.required);
    this.ctrl1 = new UntypedFormControl(null, Validators.required);
  }

  ariaValueText(current: number, max: number) {
    return `${current} out of ${max} hearts`;
  }

  ngOnInit(): void {}

  toggle = () => {
    if (this.ctrl.disabled) {
      this.ctrl.enable();
    } else {
      this.ctrl.disable();
    }
  };
}
