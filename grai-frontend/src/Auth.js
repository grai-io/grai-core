import { supabase } from './supabaseClient'

const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

function generateString(length) {
    let result = ' ';
    const charactersLength = characters.length;
    for ( let i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    return result;
}

function fromDict(dict, key, defaultValue) {
    return key in dict ? dict[key] : defaultValue
}

function camelToUnderscore(key) {
    var result = key.replace( /([A-Z])/g, " $1" );
    return result.split(' ').join('_').toLowerCase();
 }

export async function SignUpAPI(values) {
    const payload = {
        email: values.emailAddress,
        password: fromDict(values, 'password', generateString(40))
    }
    const data_keys = ['firstName', 'lastName', 'companyName', 'phoneNumber', 'location']
    const extras = {}
    data_keys.forEach(function (key, idx) {
        if (key in values){
            extras[camelToUnderscore(key)] = values[key]
        }
    })


    var result = await supabase.auth.signUp(payload)

    if (result.error){
        throw Error(result.error.message)
    }
    
    extras.id = result.user.id
    var result2 = await supabase.from('profiles').upsert(extras)

  }

  
