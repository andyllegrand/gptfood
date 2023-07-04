//
//  RecipeListView.swift
//  gptfood
//
//  Created by Andy LeGrand on 6/20/23.
//

//  FoodGPT 🍔

import SwiftUI

struct RecipeListView: View {
    @EnvironmentObject var sharedService: Service
    
    var body: some View {
        NavigationStack {
            Text("FoodGPT 🍔")
                .fontWeight(.semibold)
                .padding(.top, -30.0)
            List {
                ForEach(sharedService.recipes.indices, id: \.self) { index in
                                HStack {
                                    Text(sharedService.recipes[index].name)
                                    Spacer()
                                }
                            }
                }
                .padding()
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .navigationBarTrailing) {
                        NavigationLink {
                            IngredientListView()
                        } label: {
                            Text("Ingredients")
                        }
                    }
                    ToolbarItem(placement: .bottomBar) {
                        Button("Generate Recipe") {
                            //  Call update recipes, then get results
                            sharedService.updateRecipes()
                        }
                    }
                }
        }
        
    }
}

struct RecipeListView_Previews: PreviewProvider {
    static var previews: some View {
        RecipeListView()
    }
}
