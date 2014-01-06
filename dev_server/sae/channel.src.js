// ==ClosureCompiler==
// @output_file_name default.js
// @compilation_level SIMPLE_OPTIMIZATIONS
// @use_closure_library true
// @formatting pretty_print
// ==/ClosureCompiler==

goog.provide('sae');

goog.require('goog.dom');
goog.require('goog.net.XhrIo');
goog.require('goog.Uri.QueryData');

appengine = {};

appengine.DevSocket = function(url) {
  this.readyState = appengine.DevSocket.ReadyState.CONNECTING;
  this.token_ = url.substring(url.lastIndexOf("/") + 1);
  this.applicationKey_ = this.token_;
  this.clientId_ = null;
  this.win_ = goog.dom.getWindow();
  this.pollingTimer_ = null;
  goog.net.XhrIo.send(this.getUrl_("connect"), goog.bind(this.connect_, this));
  goog.events.listen(this.win_, "beforeunload", goog.bind(this.beforeunload_, this));
  if(!document.body) {
    throw"document.body is not defined -- do not create socket from script in <head>.";
  }
};

appengine.DevSocket.POLLING_TIMEOUT_MS = 500;
appengine.DevSocket.BASE_URL = "/_sae/channel/";
appengine.DevSocket.ReadyState = {CONNECTING:0, OPEN:1, CLOSING:2, CLOSED:3};

appengine.DevSocket.prototype.getUrl_ = function(command) {
  var url = appengine.DevSocket.BASE_URL + "dev?command=" + command + "&channel=" + this.token_;
  this.clientId_ && (url += "&client=" + this.clientId_);
  return url
};

appengine.DevSocket.prototype.connect_ = function(e) {
  var xhr = e.target;
  if(xhr.isSuccess()) {
    this.clientId_ = xhr.getResponseText(), this.readyState = appengine.DevSocket.ReadyState.OPEN, this.onopen(), this.pollingTimer_ = this.win_.setTimeout(goog.bind(this.poll_, this), appengine.DevSocket.POLLING_TIMEOUT_MS)
  }else {
    this.readyState = appengine.DevSocket.ReadyState.CLOSING;
    var evt = {};
    evt.description = xhr.getStatusText();
    evt.code = xhr.getStatus();
    this.onerror(evt);
    this.readyState = appengine.DevSocket.ReadyState.CLOSED;
    this.onclose()
  }
};

appengine.DevSocket.prototype.disconnect_ = function() {
  this.readyState = appengine.DevSocket.ReadyState.CLOSED;
  this.onclose()
};

appengine.DevSocket.prototype.forwardMessage_ = function(e) {
  var xhr = e.target;
  if(xhr.isSuccess()) {
    var evt = {};
    evt.data = xhr.getResponseText();
    if(evt.data.length) {
      this.onmessage(evt)
    }
    this.readyState == appengine.DevSocket.ReadyState.OPEN && (this.pollingTimer_ = this.win_.setTimeout(goog.bind(this.poll_, this), appengine.DevSocket.POLLING_TIMEOUT_MS))
  }else {
    evt = {}, evt.description = xhr.getStatusText(), evt.code = xhr.getStatus(), this.onerror(evt), this.readyState = appengine.DevSocket.ReadyState.CLOSED, this.onclose()
  }
};

appengine.DevSocket.prototype.poll_ = function() {
  goog.net.XhrIo.send(this.getUrl_("poll"), goog.bind(this.forwardMessage_, this))
};

appengine.DevSocket.prototype.beforeunload_ = function() {
  var xhr = goog.net.XmlHttp();
  xhr.open("GET", this.getUrl_("disconnect"), !1);
  xhr.send()
};

appengine.DevSocket.prototype.forwardSendComplete_ = function(e) {
  var xhr = e.target;
  if(!xhr.isSuccess()) {
    var evt = {};
    evt.description = xhr.getStatusText();
    evt.code = xhr.getStatus();
    this.onerror(evt)
  }
};

appengine.DevSocket.prototype.onopen = function() {};
appengine.DevSocket.prototype.onmessage = function() {};
appengine.DevSocket.prototype.onerror = function() {};
appengine.DevSocket.prototype.onclose = function() {};

appengine.DevSocket.prototype.send = function(data) {
  if(this.readyState != appengine.DevSocket.ReadyState.OPEN) {
    return!1
  }
  var url = appengine.DevSocket.BASE_URL + "message", sendData = new goog.Uri.QueryData;
  sendData.set("from", this.applicationKey_);
  sendData.set("message", data);
  goog.net.XhrIo.send(url, goog.bind(this.forwardSendComplete_, this), "POST", sendData.toString());
  return!0
};

appengine.DevSocket.prototype.close = function() {
  this.readyState = appengine.DevSocket.ReadyState.CLOSING;
  this.pollingTimer_ && this.win_.clearTimeout(this.pollingTimer_);
  goog.net.XhrIo.send(this.getUrl_("disconnect"), goog.bind(this.disconnect_, this))
};

goog.exportSymbol("sae.Channel.prototype.onopen", appengine.DevSocket.prototype.onopen);
goog.exportSymbol("sae.Channel.prototype.onmessage", appengine.DevSocket.prototype.onmessage);
goog.exportSymbol("sae.Channel.prototype.onerror", appengine.DevSocket.prototype.onerror);
goog.exportSymbol("sae.Channel.prototype.onclose", appengine.DevSocket.prototype.onclose);
goog.exportSymbol("sae.Channel", appengine.DevSocket);
goog.exportSymbol("sae.Channel.ReadyState", appengine.DevSocket.ReadyState);
goog.exportSymbol("sae.Channel.prototype.send", appengine.DevSocket.prototype.send);
goog.exportSymbol("sae.Channel.prototype.close", appengine.DevSocket.prototype.close);
