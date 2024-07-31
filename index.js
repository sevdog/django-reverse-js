
export class UrlResolver {
    constructor(prefix, patterns) {
        this.prefix = prefix;
        this.patterns = patterns;

        this.reverse = this.reverse.bind(this);
    }

    reverse(...args) {
        let validateArgs, buildKwargs;
        if (args.length === 1 && typeof (args[0]) === 'object') {
            // kwargs mode
            const providedKeys = Object.keys(args[0]);
            validateArgs = ([_urlTemplate, urlParams]) => {
                // check every needed param was provided (without extra elements)
                return urlParams.length === providedKeys.length &&
                    urlParams.every(p => providedKeys.includes(p));
            }
            // return first element
            buildKwargs = () => args[0];
        } else {
            // args mode
            // check every required param
            validateArgs = ([_urlTemplate, urlParams]) => urlParams.length === args.length;
            // build keyword-arguments from arguments
            buildKwargs = (keys) => Object.fromEntries(keys.map((key, i) => [key, args[i]]));
        }

        // search between patterns if one matches provided args
        const urlPattern = this.patterns.find(validateArgs);
        if (!urlPattern) {
            return null
        }
        const [urlTemplate, urlKwargNames] = urlPattern;
        const urlKwargs = buildKwargs(urlKwargNames);
        const url = Object.entries(urlKwargs).reduce((partialUrl, [pName, pValue]) => {
            if (pValue == null)
                pValue = '';
            // replace variable with param
            return partialUrl.replace(`%(${pName})s`, pValue);
        }, urlTemplate);
        return `${this.prefix}${url}`;
    };
}


export function factory(config) {
    const {
        urls: urlPatterns,
        prefix: urlPrefix
    } = config;

    return urlPatterns.reduce((resolver, [name, pattern]) => {
        const urlResolver = new UrlResolver(urlPrefix, pattern);
        resolver[name] = urlResolver.reverse;
        // turn snake-case into camel-case
        resolver[name.replace(/[-_]+(.)/g, (_m, p1) => p1.toUpperCase())] = urlResolver.reverse;
        // turn snake-case into dash-case
        resolver[name.replace(/-/g, '_')] = urlResolver.reverse;
        return resolver
    }, {});
}
