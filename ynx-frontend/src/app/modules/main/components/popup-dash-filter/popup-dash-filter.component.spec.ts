import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PopupDashFilterComponent } from './popup-dash-filter.component';

describe('PopupDashFilterComponent', () => {
  let component: PopupDashFilterComponent;
  let fixture: ComponentFixture<PopupDashFilterComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PopupDashFilterComponent]
    });
    fixture = TestBed.createComponent(PopupDashFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
