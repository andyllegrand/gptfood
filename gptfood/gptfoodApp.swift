//
//  gptfoodApp.swift
//  gptfood
//
//  Created by Andy LeGrand on 6/20/23.
//

import SwiftUI

@main
struct gptfoodApp: App {
    //  create 1 service instance for entire app
    @StateObject private var sharedService = Service()
    
    var body: some Scene {
        WindowGroup {
            RecipeListView()
                .environmentObject(sharedService)
        }
    }
}
