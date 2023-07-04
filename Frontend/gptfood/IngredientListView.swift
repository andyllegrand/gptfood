//
//  ContentView.swift
//  gptfood
//
//  Created by Andy LeGrand on 6/20/23.
//

import SwiftUI

struct IngredientListView: View {
    @EnvironmentObject var sharedService: Service
    @State private var newIngredientName = ""

    var body: some View {
        NavigationStack {
            Text("FoodGPT 🍔")
                .fontWeight(.semibold)
                .padding(.top, -30.0)
            
            List {
                ForEach(sharedService.ingredients.indices, id: \.self) { index in
                                HStack {
                                    Text(sharedService.ingredients[index].name)
                                    Spacer()
                                    Button(action: {
                                        sharedService.removeIngredient(at: index)
                                    }) {
                                        Image(systemName: "minus.circle")
                                            .foregroundColor(.red)
                                    }
                                }
                            }
            }
            .padding()
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                //  Using "navigationtitle" as 
                ToolbarItem(placement: .navigationBarLeading) {
                    Text("")
                }
            }
        
            HStack {
                TextField("Enter text", text: $newIngredientName)
                    .textFieldStyle(.roundedBorder)
                    .padding()
                
                Button(action: {
                    //  add new ingredient to Serice ingredient list
                    sharedService.addIngredient(new_ingredient: Ingredient(name: newIngredientName))
                    
                    //  erase textbox
                    newIngredientName = ""
                }) {
                    Text("Submit")
                            .foregroundColor(.white)
                            .padding(.horizontal, 12) // Adjust horizontal padding
                            .padding(.vertical, 8) // Adjust vertical padding
                            .background(Color.blue)
                            .font(.system(size: 14)) // Adjust font size
                            .cornerRadius(8)
                }
            }
        }
    }
}


struct ContentView_Previews: PreviewProvider {
    @StateObject private var sharedService = Service()
    static var previews: some View {
        IngredientListView().environmentObject(Service())
    }
}
