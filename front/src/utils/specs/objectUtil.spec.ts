import { expect, test } from 'vitest'
import { findValInObject, type searchIn } from "../objectUtil";

const mockedObg: searchIn = {
    fields: [{ name: 'testName', value: 'testValue', field: 'testField' }]
}

const mockedUsersObj: searchIn = {
    fields: [{ name: 'testName', value: 'testValue', field: 'users' }]
}

test('successValSearchInObject', () => {
    expect(findValInObject(mockedObg, 'testField')).toBe('testValue')
})

test('successValSearchInObject', () => {
    expect(findValInObject(mockedUsersObj, 'users')).toStrictEqual(['testValue'])
})

test('returnWithEmptyRes', () => {
    expect(findValInObject(mockedUsersObj, 'userss')).toBeUndefined()
})