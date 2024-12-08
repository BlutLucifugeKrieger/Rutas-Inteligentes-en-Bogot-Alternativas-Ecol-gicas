import { TestBed } from '@angular/core/testing';

import { RlService } from './rl.service';

describe('RlService', () => {
  let service: RlService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RlService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
