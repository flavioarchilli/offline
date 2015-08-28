/* Author: Flavio Archilli 2015                                      */
/* version 0.01                                                      */
/* set of class used in the construction of a python-like dictionary */
#ifndef HELPERS
#define HELPERS

#include <iostream>
#include <sstream>
#include <string>
#include <map>
#include <vector>
#include <ostream>

class base_object{
 public:
  base_object(){}
  virtual ~base_object(){}
  virtual std::string toString() const = 0;
  
};

template <typename T>
class _pair : public base_object{

public:
  _pair(){}
  _pair(T _x, T _y) : x(_x), y(_y) {}
  ~_pair(){}

  std::string toString() const {
    std::ostringstream ost;
    ost << "(" << x.toString() << "," << y.toString() << ")";
    return ost.str();
  }

private:
  T x;
  T y;

};

template <typename T>
class _type : public base_object{
public:
  _type(){};
  _type(T _x) : x(_x) {};
  ~_type(){}

  std::string toString() const {
    std::ostringstream ost;
    ost << x;
    return ost.str();
  }

private:
  T x;
};


// specialization of the string type
template <>
class _type<std::string> : public base_object, public std::string{
public:
  _type(){}
  _type(std::string const & _x) : std::basic_string<char>(_x) {}
  _type(char const * _x) : std::basic_string<char>(_x) {}
  ~_type(){}

  std::string toString() const {
    std::ostringstream ost;
    ost << "'" << *this << "'";
    return ost.str();
  }

};

template <typename T>
class list_of_object : public base_object{
 public:
  list_of_object(){}
  list_of_object(std::vector<T> const & _list) : list(_list){}

  std::string toString() const {
    std::ostringstream ost;
    
    //    ost << "[";
    if (!list.empty()){
      for (typename std::vector<T>::const_iterator it = list.begin(); it != list.end() -1; ++it) {
	ost << (*it).toString() << " , ";
      }
      ost << list.back().toString();      
    }
    //    ost << "]";
    return ost.str();
  }

  void push_back(T p) {
    list.push_back(p);
  }

private:
  std::vector<T> list;
};

template <typename valueT>
class _item : public base_object{
 public:
  _item(){};
  _item(std::string _key, const valueT & _value) : key(_key), value(_value) {};
  ~_item(){};

  std::string toString() const {
    std::ostringstream ost;
    
    ost << "'" << key << "': " << value.toString();
    return ost.str();
  }  

 private:
  std::string key;
  const valueT value;
};


template <>
class _item<std::string>: public base_object{
 public:
  _item(){}
  _item(std::string _key, std::string const & _value) : key(_key), value(_value) {}
  ~_item(){}
  
  std::string toString() const {
    std::ostringstream ost;
    
    ost << "'" << key << "': " << value;
    return ost.str();
  }  
  
  
 private:
  std::string key;
  const std::string value;
};


template <typename listT>
class _item<list_of_object<listT> > : public base_object{
 public:
  _item(){};
  _item(std::string _key, const list_of_object<listT> & _value) : key(_key), value(_value) {};
  ~_item(){};

  std::string toString() const {
    std::ostringstream ost;
    
    ost << "'" << key << "': [" << value.toString() << "]";
    return ost.str();
  }  

 private:
  std::string key;
  const list_of_object<listT> value;
};


#endif //HELPERS
