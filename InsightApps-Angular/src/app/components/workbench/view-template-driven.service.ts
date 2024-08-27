import { Injectable } from '@angular/core';
import { RolespriviledgesService } from './rolespriviledges.service';

@Injectable({
  providedIn: 'root'
})
export class ViewTemplateDrivenService {
// viewDashboard = false;
// viewSheets = false;
// viewSavedQueries = false;
// viewDbs = false;

  constructor(private rolesprevilgeService:RolespriviledgesService) { }

viewDtabase(){
return this.rolesprevilgeService.userHasPriviledge(4);
}
viewSheets(){
  return this.rolesprevilgeService.userHasPriviledge(20);
}
viewDashboard(){
  return this.rolesprevilgeService.userHasPriviledge(36);
}
viewCustomSql(){
  return this.rolesprevilgeService.userHasPriviledge(54);
}
editDashboard(){
  return this.rolesprevilgeService.userHasPriviledge(37);
}
ViewRoles(){
  return this.rolesprevilgeService.userHasPriviledge(59);
}
viewUsers(){
  return this.rolesprevilgeService.userHasPriviledge(71);
}

}
