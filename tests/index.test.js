import { expect } from '@jest/globals';
import {UrlResolver, factory} from '../index';
import data from './data/routes.json';

describe('Resolver argument parser', () => {
    it('Eval url with no arguments', () => {
        const resolver = new UrlResolver('/', [
            [
                "test_no_url_args",
                []
            ]
        ]);

        expect(resolver.reverse()).toBe('/test_no_url_args');
    });

    it('Eval url with one argument', () => {
        const resolver = new UrlResolver('/', [
            [
                "test_one_url_args/%(arg_one)s",
                [
                    "arg_one"
                ]
            ]
        ]);

        expect(resolver.reverse('foo')).toBe('/test_one_url_args/foo');
        expect(resolver.reverse({arg_one: 'foo'})).toBe('/test_one_url_args/foo');
    });


    it('Eval url with optional argument', () => {
        const resolver = new UrlResolver('/', [
            [
                "test_optional_url_arg/2_%(arg_two)s",
                [
                    "arg_two"
                ]
            ],
            [
                "test_optional_url_arg/1_%(arg_one)s-2_%(arg_two)s",
                [
                    "arg_one",
                    "arg_two"
                ]
            ]
        ]);

        // single argument
        expect(resolver.reverse('foo')).toBe('/test_optional_url_arg/2_foo');
        expect(resolver.reverse({arg_two: 'foo'})).toBe('/test_optional_url_arg/2_foo');
        // multi args
        expect(resolver.reverse('foo', 'bar')).toBe('/test_optional_url_arg/1_foo-2_bar');
        expect(resolver.reverse({arg_two: 'foo', arg_one: 'bar'})).toBe('/test_optional_url_arg/1_bar-2_foo');
    });
});

describe('Resolver factory', () => {
    const resolver = factory(data);

    it('Handles namespaces', () => {
        expect(resolver['ns1:test_two_url_args']('foo', 'bar')).toBe('/ns1/test_two_url_args/foo-bar');
        expect(resolver['ns2:test_two_url_args']('foo', 'bar')).toBe('/ns2/test_two_url_args/foo-bar');
    });

    it('Handles nested namespaces', () => {
        expect(resolver['nestedns:ns1:test_two_url_args']('foo', 'bar')).toBe('/nestedns/ns1/test_two_url_args/foo-bar');
    });

    it('Handles different cases', () => {
        expect(resolver.testNoUrlArgs()).toBe('/test_no_url_args');
        expect(resolver['test_no_url_args']()).toBe('/test_no_url_args');
    });

    it('Handles duplicates argcount', () => {

        expect(resolver['test_duplicate_argcount']('foo')).toBe('/test_duplicate_argcount/-foo/');
        expect(resolver['test_duplicate_argcount']({arg_one: 'foo'})).toBe('/test_duplicate_argcount/foo-/');
        expect(resolver['test_duplicate_argcount']({arg_two: 'foo'})).toBe('/test_duplicate_argcount/-foo/');
    });
});
