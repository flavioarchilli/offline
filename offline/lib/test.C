#include "helpers.h"
#include "libHistograms.h"
#include "TFile.h"
#include "TObject.h"
#include "TStopwatch.h"

int main(){

  TStopwatch sw;
  TFile *f = TFile::Open("histograms.root","r");
  TObject *o = f->Get("histogram_0");
  // I don't care how much time it takes to open the file and read the histograms
  // I'd like to test the dictionary production.
  sw.Start();

  std::cout << getInfo(o) << std::endl;   
  sw.Stop();

  sw.Print();

  return 0;
}
