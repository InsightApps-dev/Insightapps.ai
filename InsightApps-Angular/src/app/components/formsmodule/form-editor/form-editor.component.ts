import { Component } from '@angular/core';
import { FormGroup, FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AngularEditorConfig, AngularEditorModule } from '@kolkov/angular-editor';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgSelectModule } from '@ng-select/ng-select';
import { Editor, NgxEditorModule, Toolbar, Validators } from 'ngx-editor';
import { SharedModule } from '../../../shared/sharedmodule';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-form-editor',
  standalone: true,
  imports: [SharedModule,NgSelectModule,NgbModule,   AngularEditorModule ,HttpClientModule,NgxEditorModule,FormsModule,ReactiveFormsModule],
  templateUrl: './form-editor.component.html',
  styleUrls: ['./form-editor.component.scss']
})
export class FormEditorComponent {
  htmlContent:string = '';
  config1: AngularEditorConfig = {
    editable: true,
    spellcheck: true,
    height: '15rem',
    minHeight: '5rem',
    placeholder: `'Enter text here...'`, 
    translate: 'no',
    defaultParagraphSeparator: 'p',
    defaultFontName: 'Arial',
    toolbarHiddenButtons: [
      ['bold']
      ],
    customClasses: [
      {
        name: "quote",
        class: "quote",
      },
      {
        name: 'redText',
        class: 'redText'
      },
      {
        name: "titleText",
        class: "titleText",
        tag: "h1",
      },
    ]
  };
  ngOnInit(){
    this.editor = new Editor();
  
  }
    // ngx-editor
    public editorContent!: FormGroup;
    editordoc = '';
    public editor!: Editor;
    toolbar: Toolbar = [
      ['bold', 'italic'],
      ['underline', 'strike'],
      ['code', 'blockquote'],
      ['ordered_list', 'bullet_list'],
      [{ heading: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] }],
      ['text_color', 'background_color'],
      ['align_left', 'align_center', 'align_right', 'align_justify'],
    ];
  
    form: any = new FormGroup({
      editorContent: new FormControl(
        { value: `Type Text Here`, disabled: false },
        Validators.required()
      ),
    });
}
