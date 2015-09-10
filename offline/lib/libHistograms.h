#ifndef LIB_HISTO
#define LIB_HISTO

#include "helpers.h"
#include "TObject.h"
#include "TProfile.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TAxis.h"
#include "TFile.h"

typedef _type<int> int_type;
typedef _type<float> float_type;
typedef _type<double> double_type;
typedef _type<std::string> string_type;

typedef _pair<int_type> int_pair;
typedef _pair<float_type> float_pair;
typedef _pair<double_type> double_pair;
typedef _pair<string_type> string_pair;

typedef _item<int_type> int_item;
typedef _item<float_type> float_item;
typedef _item<double_type> double_item;
typedef _item<string_type> string_item;

//template <typename T>
//std::string get1DHistoInfo(T *o);
//std::string get2DHistoInfo(T *o);
std::string getInfo(TObject *o);
std::string getDictionary(TFile *f,const char* objname);


#endif // LIB_HISTO
