//
//  shareApp.swift
//  share
//
//  Created by lyndskg on 8/6/23.
//

import SwiftUI

@main
struct shareApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
