//
//  gptfoodApp.swift
//  gptfood
//
//  Created by Andy LeGrand on 6/20/23.
//

import SwiftUI


@main
struct gptfoodApp: App {
    //@UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    @StateObject private var sharedService = Service()
    
    var body: some Scene {
        WindowGroup {
            RecipeListView()
                .environmentObject(sharedService)
        }
    }
}
