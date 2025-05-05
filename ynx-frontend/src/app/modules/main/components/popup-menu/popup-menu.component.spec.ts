import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PopupMenuComponent } from './popup-menu.component';

describe('PopupMenuComponent', () => {
  let component: PopupMenuComponent;
  let fixture: ComponentFixture<PopupMenuComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PopupMenuComponent]
    });
    fixture = TestBed.createComponent(PopupMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
