//
//  util.swift
//  gptfood
//
//  Created by Andy LeGrand on 6/20/23.
//

import Foundation

//  config settings
struct Settings {
    var server_ip: String
}

//  Ingredient user inputs. Could add additional functionality in the future
struct Ingredient: Identifiable, Codable {
    let id: UUID
    let name: String

    init(name: String) {
        self.id = UUID()
        self.name = name
    }
}

//  Recipe recieved from backend.
struct Recipe: Identifiable, Codable {
    let id: UUID
    let name: String

    init(name: String) {
        self.id = UUID()
        self.name = name
    }
}
