import { Component, ViewChild } from '@angular/core';
import { DropzoneComponent, DropzoneConfigInterface, DropzoneDirective } from 'ngx-dropzone-wrapper';
import { FilePondComponent } from 'ngx-filepond';
import * as FilePond from 'filepond';
import { FilePondModule } from "ngx-filepond";
import { FormGroup, FormControl, FormsModule, ReactiveFormsModule, Validators, FormBuilder } from '@angular/forms';
import { NgxColorsModule, validColorValidator } from 'ngx-colors';
import flatpickr from 'flatpickr';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgSelectModule } from '@ng-select/ng-select';
import { SharedModule } from '../../../shared/sharedmodule';
import { FlatpickrDefaults, FlatpickrModule } from 'angularx-flatpickr';
import { ColorPickerModule } from 'ngx-color-picker';


@Component({
  selector: 'app-form-advanced',
  standalone: true,
  imports: [SharedModule,NgSelectModule,NgbModule,FormsModule,ReactiveFormsModule,FlatpickrModule,NgxColorsModule,ColorPickerModule,FilePondModule],
  providers:[FlatpickrDefaults],
  templateUrl: './form-advanced.component.html',
  styleUrls: ['./form-advanced.component.scss']
})
export class FormAdvancedComponent {
  selectedCompanies: any=['one','two','three','four'];
  companies: any[] = ['One','Two'];
  uniqueOptions=['child1','child2']
  email: string = '';
  emailFormControl = new FormControl('', [
    Validators.required,
    Validators.email,
  ]);
  @ViewChild("myPond") myPond!: FilePondComponent;

  pondOptions: FilePond.FilePondOptions = {
    allowMultiple: true,
    labelIdle: "Drop files here to Upload...",
  };
  singlepondOptions: FilePond.FilePondOptions = {
    allowMultiple: false,
    labelIdle: "Drop files here to Upload...",
  };

  pondFiles: FilePond.FilePondOptions["files"] = [
    // {
    //   source: "assets/photo.jpeg",
    //   options: {
    //     type: "local",
    //   },
    // },

  ];

  pondHandleInit() {
    console.log("FilePond has initialised", this.myPond);
  }

  pondHandleAddFile(event: any) {
    console.log("A file was added", event);
  }

  pondHandleActivateFile(event: any) {
    console.log("A file was activated", event);
  }
  public type: string = 'component';

  public disabled: boolean = false;

  public config: DropzoneConfigInterface = {
    clickable: true,
    maxFiles: 100,
    autoReset: null,
    errorReset: null,
    cancelReset: null
  };
  @ViewChild(DropzoneComponent, { static: false }) componentRef?: DropzoneComponent;
  @ViewChild(DropzoneDirective, { static: false }) directiveRef?: DropzoneDirective;
  public resetDropzoneUploads(): void {
    if (this.type === 'directive' && this.directiveRef) {
      this.directiveRef.reset();
    } else if (this.type === 'component' && this.componentRef && this.componentRef.directiveRef) {
      this.componentRef.directiveRef.reset();
    }
  }

  public onUploadInit(args: any): void {
    console.log('onUploadInit:', args);
  }

  public onUploadError(args: any): void {
    console.log('onUploadError:', args);
  }

  public onUploadSuccess(args: any): void {
    console.log('onUploadSuccess:', args);
  }
  public color1 = `#a68e5e`;

  public exampleForm: FormGroup = new FormGroup(
    {
      inputCtrl: new FormControl("rgb(79, 195, 255)", validColorValidator()),
      pickerCtrl: new FormControl("rgb(79, 195, 255)"),
    },
    { updateOn: "change" }
  );

  ngOnInit(): void {
    this.flatpickrOptions = {
      enableTime: true,
      noCalendar: true,
      dateFormat: 'H:i',
    };
 
    flatpickr('#inlinetime', this.flatpickrOptions);
 
      this.flatpickrOptions = {
        enableTime: true,
        dateFormat: 'Y-m-d H:i', // Specify the format you want
        defaultDate: '2023-11-07 14:30', // Set the default/preloaded time (adjust this to your desired time)
      };
 
      flatpickr('#pretime', this.flatpickrOptions);
    this.exampleForm.controls["inputCtrl"].valueChanges.subscribe((color) => {
      if (this.exampleForm.controls["pickerCtrl"].valid) {
        this.exampleForm.controls["pickerCtrl"].setValue(color, {
          emitEvent: false,
        });
      }
    });
    this.exampleForm.controls["pickerCtrl"].valueChanges.subscribe((color) =>
      this.exampleForm.controls["inputCtrl"].setValue(color, {
        emitEvent: false,
      })
    );
  }

 color:string = '#EC407A';
 color2:string = '#EC407B';
 basicDemoValue = '2017-01-01';
 inlineDatePicker: Date = new Date();
 timePicker: Date | null = null;
 timePicker1: Date | null = null;
 timePicker2: Date | null = null;
 timePicker3: Date | null = null;
 timePicker4: Date | null = null;

 flatpickrOptions: any = {
   inline: true,
 };
 // flatpickrOptions: FlatpickrOptions;
 myGroup: FormGroup;
 constructor(private fb: FormBuilder) {
  // Initialize the form group and controls in the constructor
  this.myGroup = this.fb.group({
    firstName: new FormControl()
  });
 }
 selectedAccount = 'Adam';
 accounts = [
   {
     name: 'Adam',
     email: 'adam@email.com',
     age: 12,
     country: 'United States',
     child: { state: 'Active' },
   },
   {
     name: 'Homer',
     email: 'homer@email.com',
     age: 47,
     country: '',
     child: { state: 'Active' },
   },
   {
     name: 'Samantha',
     email: 'samantha@email.com',
     age: 30,
     country: 'United States',
     child: { state: 'Active' },
   },
   {
     name: 'Amalie',
     email: 'amalie@email.com',
     age: 12,
     country: 'Argentina',
     child: { state: 'Active' },
   },
   {
     name: 'Estefanía',
     email: 'estefania@email.com',
     age: 21,
     country: 'Argentina',
     child: { state: 'Active' },
   },
   {
     name: 'Adrian',
     email: 'adrian@email.com',
     age: 21,
     country: 'Ecuador',
     child: { state: 'Active' },
   },
   {
     name: 'Wladimir',
     email: 'wladimir@email.com',
     age: 30,
     country: 'Ecuador',
     child: { state: 'Inactive' },
   },
   {
     name: 'Natasha',
     email: 'natasha@email.com',
     age: 54,
     country: 'Ecuador',
     child: { state: 'Inactive' },
   },
   {
     name: 'Nicole',
     email: 'nicole@email.com',
     age: 43,
     country: 'Colombia',
     child: { state: 'Inactive' },
   },
   {
     name: 'Michael',
     email: 'michael@email.com',
     age: 15,
     country: 'Colombia',
     child: { state: 'Inactive' },
   },
   {
     name: 'Nicolás',
     email: 'nicole@email.com',
     age: 43,
     country: 'Colombia',
     child: { state: 'Inactive' },
   },
 ];
 groupByFn = (item: any) => item.child.state;

 groupValueFn = (_: string, children: any[]) => ({
   name: children[0].child.state,
   total: children.length,
 });



 addTagFn(name: any) {
   return { name: name, tag: true };
 }
 multiSelectSelected = ['Manchester'];
 multiSelect = [
   {
     name: 'London',
     child: { state: 'UK' },
   },
   {
     name: 'Liverpool',
     child: { state: 'UK' },
   },
   {
     name: 'Paris',
     child: { state: 'FR' },
   },
   {
     name: 'Lyon',
     child: { state: 'FR' },
   },
   {
     name: 'Marseille',
     child: { state: 'FR' },
   },
   {
     name: 'Hamburg',
     child: { state: 'DE' },
   },
   {
     name: 'Munich',
     child: { state: 'DE' },
   },
   {
     name: 'Berlin',
     child: { state: 'DE' },
   },
   {
     name: 'New York',
     child: { state: 'US' },
   },
   {
     name: 'Washington',
     child: { state: 'US' },
   },
   {
     name: 'Michigan',
     child: { state: 'US' },
   },
   {
     name: 'Madrid',
     child: { state: 'SP' },
   },
   {
     name: 'Barcelona',
     child: { state: 'SP' },
   },
   {
     name: 'Malaga',
     child: { state: 'SP' },
   },
 ];

}
