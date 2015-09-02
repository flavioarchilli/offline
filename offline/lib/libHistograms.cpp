#include "libHistograms.h"

std::string get1DHistoInfo(TH1D *o) {

  std::ostringstream ost; 

  std::string type(o->ClassName());
  type.erase(type.begin()); 
  double numberEntries = o->GetEntries();
  double integral = o->Integral();
  double mean = o->GetMean();
  double RMS = o->GetRMS();
  //  double skewness = o->GetSkewness();
  TAxis *xaxis = o->GetXaxis();
  TAxis *yaxis = o->GetYaxis();
  string_pair axis_titles(xaxis->GetTitle(),yaxis->GetTitle());
  int nbins = xaxis->GetNbins();

  list_of_object<double_type> values;
  list_of_object<double_pair> binning;
  list_of_object<double_pair> uncertainties;

  for(int i = 1; i<nbins+1; i++) {    
    values.push_back(double_type(o->GetBinContent(i))); 
    binning.push_back(double_pair((double_type)xaxis->GetBinLowEdge(i), (double_type)xaxis->GetBinUpEdge(i)));
    uncertainties.push_back(double_pair((double_type)o->GetBinErrorLow(i), (double_type)o->GetBinErrorUp(i)));
    
  }

  ost << "{" 
      << string_item("type",type).toString() << ", "
      << int_item("numberEntries",numberEntries).toString() << ", "
      << double_item("integral" , integral).toString() << ", "
      << double_item("mean",mean).toString() << ", "
      << double_item("RMS",RMS).toString() << ", "
    //      << double_item("skewness",skewness).toString() << ", "
      << int_item("nbins",nbins).toString() << ", "
      << _item<string_pair>("axis_titles",axis_titles).toString() << ", "
      << _item<list_of_object<double_type> >("values",values).toString() << ", "
      << _item<list_of_object<double_pair> >("binning",binning).toString() << ", "
      << _item<list_of_object<double_pair> >("uncertainties",uncertainties).toString() 
      << "}";
  return ost.str();

}

std::string get2DHistoInfo(TH2D *o) {
  
  std::ostringstream ost; 

  std::string type(o->ClassName());
  type.erase(type.begin());
  double numberEntries = o->GetEntries();
  double integral = o->Integral();
  double mean = o->GetMean();
  double RMS = o->GetRMS();
  //  double skewness = o->GetSkewness();
  TAxis *xaxis = o->GetXaxis();
  TAxis *yaxis = o->GetYaxis();
  string_pair axis_titles(xaxis->GetTitle(),yaxis->GetTitle());
  int xnbins = xaxis->GetNbins();
  int ynbins = yaxis->GetNbins();
  int nbins = xnbins*ynbins;

  list_of_object<double_type> values;
  list_of_object<double_pair> xbinning;
  list_of_object<double_pair> ybinning;
  list_of_object<double_pair> uncertainties;

  bool store(true);
  for(int i = 1; i<xnbins+1; i++) {
    xbinning.push_back(double_pair((double_type)xaxis->GetBinLowEdge(i), (double_type)xaxis->GetBinUpEdge(i)));
    for(int j = 1; j<ynbins+1; j++) {
      values.push_back(double_type(o->GetBinContent(i,j)));             
      if (store) ybinning.push_back(double_pair((double_type)yaxis->GetBinLowEdge(j), (double_type)yaxis->GetBinUpEdge(j)));
      uncertainties.push_back(double_pair((double_type)o->GetBinErrorLow(i,j), (double_type)o->GetBinErrorUp(i,j)));
    }
    store = false;
  }

  ost << "{" 
      << string_item("type",type).toString() << ", "
      << int_item("numberEntries",numberEntries).toString() << ", "
      << double_item("integral" , integral).toString() << ", "
      << double_item("mean",mean).toString() << ", "
      << double_item("RMS",RMS).toString() << ", "
    //      << double_item("skewness",skewness).toString() << ", "
      << int_item("nbins",nbins).toString() << ", "
      << int_item("xnbins",nbins).toString() << ", "
      << int_item("ynbins",nbins).toString() << ", "
      << _item<string_pair>("axis_titles",axis_titles).toString() << ", "
      << _item<list_of_object<double_type> >("values",values).toString() << ", "
      << _item<list_of_object<double_pair> >("xbinning",xbinning).toString() << ", "
      << _item<list_of_object<double_pair> >("ybinning",ybinning).toString() << ", "
      << _item<list_of_object<double_pair> >("uncertainties",uncertainties).toString() 
      << "}";
  return ost.str();

}

std::string getInfo(TObject * o){

  std::ostringstream ost;
  std::string data;

  std::string class_name = o->ClassName();
  if (!class_name.compare("TH1D") || !class_name.compare("TProfile")) {    
    data = get1DHistoInfo((TH1D*) o);
    
  } else if (!class_name.compare("TH2F")){
    data = get2DHistoInfo((TH2D*) o);

  }

  _item<std::string> key_data("key_data",data);

  ost << "{" << key_data.toString() << ", "
    << string_item("key_class", (string_type) o->ClassName()).toString() << ", "
    << string_item("key_title", (string_type) o->GetTitle()).toString() << ", "
    << string_item("key_name", (string_type) o->GetName()).toString() 
    << "}"; 
    
  return ost.str();
}


std::string getDictionary(TFile* f, const char*  objname){
  TObject *o = f->Get(objname);
  std::ostringstream ost;
  if (f->IsZombie()){
    ost << "{ 'success': False, 'message': 'Could not find key " << objname 
	<< " in file " << f->GetName() << "'}";
    return ost.str();
  }

  if (!o) {
    ost << "{ 'success': False, 'message': 'Could not open file " << f->GetName() << "'}";    
  } else {
    ost << "{ 'success': True, 'data': " << getInfo(o) << "}"; 
  }

  return ost.str();

}
