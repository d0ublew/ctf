Java.perform(function () {
  var str = Java.use("java.lang.String");
  str.equals.overload("java.lang.Object").implementation = function (obj) {
    var response = str.equals.overload("java.lang.Object").call(this, obj);
    send(
      "Is " +
        str.toString.call(this) +
        " == " +
        obj.toString() +
        " ? " +
        response
    );
    return response;
  };
});
