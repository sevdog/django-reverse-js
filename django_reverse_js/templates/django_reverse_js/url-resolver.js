{{ js_name }} = (function () {
    "use strict";
    var data = {{ data }};
    function factory(d) {
        var urlPatterns = d.urls;
        var urlPrefix = d.prefix;
        var Urls = {};
        var selfUrlPatterns = {};

        function _getUrl (urlPattern) {
            return function () {
                var _arguments, url, urlArg, urlArgs, _i, _ref,
                _refList, matchRef, providedKeys, buildKwargs;

                _arguments = arguments;
                _refList = selfUrlPatterns[urlPattern];

                if (arguments.length === 1 && typeof (arguments[0]) === "object") {
                    // kwargs mode
                    var providedKeyList = Object.keys (arguments[0]);
                    providedKeys = {};
                    for (_i = 0; _i < providedKeyList.length; _i++)
                        providedKeys[providedKeyList[_i]] = 1;

                    matchRef = function (ref) {
                        var _i;

                        // Verify that they have the same number of arguments
                        if (ref[1].length !== providedKeyList.length)
                            return false;

                        for (_i = 0; _i < ref[1].length && ref[1][_i] in providedKeys;_i++);

                        // If for loop completed, we have all keys
                        return _i === ref[1].length;
                    }

                    buildKwargs = function (keys) {return _arguments[0];}
                } else {
                    // args mode
                    matchRef = function (ref) {
                        return ref[1].length === _arguments.length;
                    }

                    buildKwargs = function (keys) {
                        var kwargs = {};

                        for (var i = 0; i < keys.length; i++) {
                            kwargs[keys[i]] = _arguments[i];
                        }

                        return kwargs;
                    }
                }

                for (_i = 0; _i < _refList.length && !matchRef(_refList[_i]); _i++);

                // can't find a match
                if (_i === _refList.length)
                    return null;

                _ref = _refList[_i];
                url = _ref[0];
                urlArgs = buildKwargs(_ref[1]);
                for (urlArg in urlArgs) {
                    var urlArgValue = urlArgs[urlArg];
                    if (urlArgValue === undefined || urlArgValue === null) {
                        urlArgValue = '';
                    } else {
                        urlArgValue = urlArgValue.toString();
                    }
                    url = url.replace("%(" + urlArg + ")s", urlArgValue);
                }
                return urlPrefix + url;
            };
        };

        var name, pattern, url, _i, _len, _ref;
        for (_i = 0, _len = urlPatterns.length; _i < _len; _i++) {
            _ref = urlPatterns[_i];
            name = _ref[0];
            pattern = _ref[1];
            selfUrlPatterns[name] = pattern;
            url = _getUrl(name);
            Urls[name.replace(/[-_]+(.)/g, function (_m, p1) { return p1.toUpperCase(); })] = url;
            Urls[name.replace(/-/g, '_')] = url;
            Urls[name] = url;
        }

        return Urls;
    }
    return data ? factory(data) : factory;
})();
