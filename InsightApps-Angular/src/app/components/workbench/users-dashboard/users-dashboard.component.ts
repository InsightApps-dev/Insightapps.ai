import { CommonModule } from '@angular/common';
import { Component, ViewChild } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgxPaginationModule } from 'ngx-pagination';
import { SharedModule } from '../../../shared/sharedmodule';
import { WorkbenchService } from '../workbench.service';
import Swal from 'sweetalert2';
import { PasswordValidators } from '../../../shared/password-validator';
import { InsightsButtonComponent } from '../insights-button/insights-button.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-users-dashboard',
  standalone: true,
  imports: [SharedModule,CommonModule,FormsModule,NgbModule,NgxPaginationModule,ReactiveFormsModule,InsightsButtonComponent],
  templateUrl: './users-dashboard.component.html',
  styleUrl: './users-dashboard.component.scss'
})
export class UsersDashboardComponent {
  gridView = true;
  userName ='';
  itemsPerPage:any;
  pageNo = 1;
  page: number = 1;
  totalItems:any;
  savedUsersList =[] as any;
  userAddedRolesList =[] as any;
  searchUser :any
  addUserForm:FormGroup;
  confirmPasswordError = false;
  userEditHidePassword = false;
  addUserDivForm = false;
  allSelected = false;
  userId:any;
  @ViewChild('Adduser') Adduser : any;

  constructor(public modalService:NgbModal,private workbechService:WorkbenchService,private formBuilder:FormBuilder,private router:Router){
    this.addUserForm = this.formBuilder.group({
      username: ['', Validators.required],
      firstname:['', Validators.required],
      lastname:['', Validators.required],
      role: this.formBuilder.array([]),
      is_active:[''],
      email:['',[Validators.required, Validators.pattern('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$')],],
      password: ['', [Validators.required, Validators.compose([
        Validators.required,
        Validators.minLength(8),
        PasswordValidators.patternValidator(new RegExp("(?=.*[0-9])"), {
          requiresDigit: true
        }),
        PasswordValidators.patternValidator(new RegExp("(?=.*[A-Z])"), {
          requiresUppercase: true
        }),
        PasswordValidators.patternValidator(new RegExp("(?=.*[a-z])"), {
          requiresLowercase: true
        }),
        PasswordValidators.patternValidator(new RegExp("(?=.*[$@^!%*?&])"), {
          requiresSpecialChars: true
        })
        ])]],
      conformpassword: ['', Validators.required],
    })
    if(this.router.url.includes('/workbenchdashboard/user-add')){
      this.addUserDiv();
    }
    if(this.router.url.includes('/workbenchdashboard/roles-list/dashboard')){
      this.addUserDivForm= false;
    }
  }

  ngOnInit(){
    this.getUserList()
  }
  get role(): FormArray {
    return this.addUserForm .get('role') as FormArray;
  }
  get f() {
    return this.addUserForm.controls;
  }
  get passwordValid() {
    return this.addUserForm.controls["password"].errors === null;
  }
  
  get requiredValid() {
    return !this.addUserForm.controls["password"].hasError("required");
  }
  
  get minLengthValid() {
    return !this.addUserForm.controls["password"].hasError("minlength");
  }
  
  get requiresDigitValid() {
    return !this.addUserForm.controls["password"].hasError("requiresDigit");
  }
  
  get requiresUppercaseValid() {
    return !this.addUserForm.controls["password"].hasError("requiresUppercase");
  }
  
  get requiresLowercaseValid() {
    return !this.addUserForm.controls["password"].hasError("requiresLowercase");
  }
  
  get requiresSpecialCharsValid() {
    return !this.addUserForm.controls["password"].hasError("requiresSpecialChars");
  }
  checkConfirmPassword(){
    if(this.addUserForm.value.conformpassword === this.addUserForm.value.password ){
      this.confirmPasswordError = false;
    } else{
      this.confirmPasswordError = true;
    }
  }
showPassword = false;
showPassword1 = false;
toggleClass = "off-line";
toggleClass1 = "off-line";
  toggleVisibility() {
    this.showPassword = !this.showPassword;
    if (this.toggleClass === "off-line") {
      this.toggleClass = "line";
    } else {
      this.toggleClass = "off-line";
    }
  }
  toggleVisibility1() {
    this.showPassword1 = !this.showPassword1;
    if (this.toggleClass1 === "off-line") {
      this.toggleClass1 = "line";
    } else {
      this.toggleClass1 = "off-line";
    }
  }

  searchUserList(){
    this.pageNo=1
    this.getUserList();
  }
  pageChangegetUserList(pageNo:any){
    this.pageNo=pageNo;
    this.getUserList();
  }
  getUserList(){
    const obj ={
      search : this.searchUser,
      page_no:this.pageNo,
    page_count:this.itemsPerPage
    }
    if(obj.search === '' || obj.search === null){
      delete obj.search
    }
    if(obj.page_count == undefined || obj.page_count == null){
      delete obj.page_count;
    }
    this.workbechService.getUserList(obj).subscribe({
      next:(data)=>{
        console.log(data);
        this.savedUsersList=data.sheets;
        this.itemsPerPage = data.items_per_page;
        this.totalItems = data.total_items;
       },
      error:(error)=>{
        console.log(error);
        Swal.fire({
          icon: 'error',
          title: 'oops!',
          text: error.error.message,
          width: '400px',
        })
      }
    }) 
  }

  // addUserModal(OpenmdoModal: any) {
  //   this.addUserForm.reset();
  //   this.modalService.open(OpenmdoModal);
  //   this.getAddedRolesList();
  //   this.userEditHidePassword= false;
  // }

  addUserDiv() {
    this.addUserDivForm = true;
    this.addUserForm.reset();
    this.getAddedRolesList();
    this.userEditHidePassword = false;
    const rolesArray = this.addUserForm.get('role') as FormArray;
    if (rolesArray && rolesArray instanceof FormArray) {
      rolesArray.clear(); // Clear the current FormArray
      }
  }
  closeAddUserForm(){
    this.addUserDivForm = false;
  }

  setRoles() {
    const rolesArray = this.addUserForm.get('role') as FormArray;
    rolesArray.clear(); // Clear the FormArray

    this.userAddedRolesList.forEach(() => {
      rolesArray.push(this.formBuilder.control(false)); // Add a control for each role
    });

    rolesArray.valueChanges.subscribe(values => {
      this.allSelected = values.every((val: boolean) => val === true);
    });
  }

  toggleSelectAll() {
    const rolesArray = this.addUserForm.get('role') as FormArray;
    const shouldSelectAll = !this.allSelected;

    rolesArray.controls.forEach((control, index) => {
      control.setValue(shouldSelectAll ? this.userAddedRolesList[index] : false);
    });

    this.allSelected = shouldSelectAll;
    this.getSelectedRoles();

  }

  onCheckboxChange() {
    const rolesArray = this.addUserForm.get('role') as FormArray;
    if (rolesArray && rolesArray instanceof FormArray) {
      const allSelected = rolesArray.controls.every(control => control.value);
      this.allSelected = allSelected;
    }
    // this.getSelectedRoles();
  }
  getSelectedRoles() {
    const rolesArray = this.addUserForm.get('role') as FormArray;
    // Filter to get only the selected roles
    const selectedRoles = this.userAddedRolesList
        .filter((role: any, index: number) => rolesArray.at(index).value)
        .map((role: any) => role); // This will give you the actual role names instead of true/false
    console.log('Selected roles:', selectedRoles);
    return selectedRoles;
  }
  gotoAddRole(){
    this.router.navigate(['/workbench/dashboard/role-add'])
  }
getAddedRolesList(){
  this.workbechService.getAddedRolesList().subscribe({
    next:(data)=>{
      console.log(data);
      this.userAddedRolesList=data;
      this.setRoles();
     },
    error:(error)=>{
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'oops!',
        text: error.error.message,
        width: '400px',
      })
    }
  }) 
}

addUser(){
  const selectedRoles = this.getSelectedRoles(); // Get the selected roles
  const userData = {
      ...this.addUserForm.value,
      role: selectedRoles // Replace the roles array with the selected roles
  };
    this.workbechService.addUserwithRoles(userData  ).subscribe({
    next:(data)=>{
      console.log(data);
      this.addUserDivForm = false;
      Swal.fire({
        icon: 'success',
        title: 'Done!',
        text: data.message,
        width: '400px',
      })
      this.getUserList();
     },
    error:(error)=>{
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'oops!',
        text: error.error.message,
        width: '400px',
      })
    }
  }) 
}
deleteUser(id:any){
  Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, delete it!'
  }).then((result)=>{
    if(result.isConfirmed){
      this.workbechService.deleteUser(id)
      .subscribe(
        {
          next:(data:any) => {
            console.log(data);      
            if(data){
              Swal.fire({
                icon: 'success',
                title: 'Deleted!',
                text: 'User Deleted Successfully',
                width: '400px',
              })
            }
            this.getUserList();
          },
          error:(error:any)=>{
            Swal.fire({
              icon: 'warning',
              text: error.error.message,
              width: '300px',
            })
            console.log(error)
          }
        } 
      )
    }})
}


getUserIdDetails(id:any){
  this.userId = id;
  this.userEditHidePassword = true;
  this.addUserDivForm = true;
  this.workbechService.getUserIdDetails(id)
  .subscribe(
    {
      next:(data:any) => {
        console.log(data); 
        this.addUserForm.patchValue({
          firstname:data.firstname,
          lastname:data.lastname,
          username:data.username,
          email:data.email,
          is_active:data.is_active,
        })     
        this.userAddedRolesList = data.role;
        this.setRoles();
        this.patchRoles(data.role);
      },
      error:(error:any)=>{
        Swal.fire({
          icon: 'warning',
          text: error.error.message,
          width: '300px',
        })
        console.log(error)
      }
    } 
  )
}
patchRoles(selectedRoles: string[]) {
  const rolesArray = this.addUserForm.get('role') as FormArray;

  if (rolesArray && rolesArray instanceof FormArray) {
    rolesArray.clear(); // Clear the current FormArray

    // Add only the selected roles
    selectedRoles.forEach((role) => {
      if (this.userAddedRolesList.includes(role)) {
        rolesArray.push(this.formBuilder.control(true));
      }
    });

    // Sync the 'allSelected' flag based on whether all roles are selected
    this.allSelected = selectedRoles.length === this.userAddedRolesList.length;
  }
}

editUser(){
  const selectedRoles = this.getSelectedRoles(); // Get the selected roles
  const userData = {
      ...this.addUserForm.value,
      role: selectedRoles // Replace the roles array with the selected roles
  };
  delete userData.password;
    delete userData.conformpassword;
    this.workbechService.editUser(this.userId,userData).subscribe({
    next:(data)=>{
      console.log(data);
      this.addUserDivForm = false;
      Swal.fire({
        icon: 'success',
        title: 'Done!',
        text: data.message,
        width: '400px',
      })
      this.getUserList();
     },
    error:(error)=>{
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'oops!',
        text: error.error.message,
        width: '400px',
      })
    }
  }) 
}
}
